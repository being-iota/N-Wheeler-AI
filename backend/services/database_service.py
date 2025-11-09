"""
Database service for CRUD operations
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from database.connection import get_db, mongo_db, redis_client
from database.models import Vehicle, Appointment, Feedback, Alert, Conversation
import uuid
import json


class DatabaseService:
    """
    Service for database operations
    """
    
    def __init__(self):
        from database.connection import mongo_db, redis_client
        self.mongo_collection = mongo_db.telematics_data if mongo_db else None
        self.redis = redis_client
    
    def get_db_session(self):
        """Get database session"""
        from database.connection import SessionLocal
        if SessionLocal is None:
            raise Exception("PostgreSQL database is not connected")
        return next(get_db())
    
    async def store_telematics_data(self, vehicle_id: str, sensor_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Store telematics data in MongoDB"""
        if self.mongo_collection is None:
            return  # Skip if MongoDB is not available
        
        document = {
            "vehicle_id": vehicle_id,
            "sensor_data": sensor_data,
            "analysis": analysis,
            "timestamp": datetime.utcnow()
        }
        self.mongo_collection.insert_one(document)
        
        # Also cache latest data in Redis
        if self.redis:
            try:
                self.redis.setex(
                    f"telematics:{vehicle_id}:latest",
                    3600,  # 1 hour TTL
                    json.dumps(document, default=str)
                )
            except Exception:
                pass  # Skip if Redis is not available
    
    async def get_latest_analysis(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """Get latest analysis for a vehicle"""
        # Try Redis first
        cached = self.redis.get(f"telematics:{vehicle_id}:latest")
        if cached:
            return json.loads(cached)
        
        # Fall back to MongoDB
        latest = self.mongo_collection.find_one(
            {"vehicle_id": vehicle_id},
            sort=[("timestamp", -1)]
        )
        
        if latest:
            latest["_id"] = str(latest["_id"])
            return latest
        
        return None
    
    async def store_predictions(self, vehicle_id: str, predictions: Dict[str, Any]):
        """Store failure predictions"""
        # Store in MongoDB
        document = {
            "vehicle_id": vehicle_id,
            "predictions": predictions,
            "timestamp": datetime.utcnow()
        }
        mongo_db.predictions.insert_one(document)
        
        # Cache in Redis
        self.redis.setex(
            f"predictions:{vehicle_id}:latest",
            3600,
            json.dumps(predictions, default=str)
        )
    
    async def get_latest_predictions(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """Get latest predictions for a vehicle"""
        cached = self.redis.get(f"predictions:{vehicle_id}:latest")
        if cached:
            return json.loads(cached)
        
        latest = mongo_db.predictions.find_one(
            {"vehicle_id": vehicle_id},
            sort=[("timestamp", -1)]
        )
        
        if latest:
            latest["_id"] = str(latest["_id"])
            return latest.get("predictions")
        
        return None
    
    async def store_appointment(self, appointment_data: Dict[str, Any]):
        """Store appointment"""
        db = self.get_db_session()
        try:
            appointment = Appointment(
                id=str(uuid.uuid4()),
                vehicle_id=appointment_data["vehicle_id"],
                service_type=appointment_data["service_type"],
                date=datetime.fromisoformat(appointment_data["date"]),
                time=appointment_data["time"],
                status=appointment_data.get("status", "scheduled"),
                estimated_duration=appointment_data.get("estimated_duration", 60)
            )
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
        finally:
            db.close()
    
    async def get_appointments_by_date(self, appointment_date: date) -> List[Dict[str, Any]]:
        """Get appointments for a specific date"""
        db = self.get_db_session()
        try:
            start_datetime = datetime.combine(appointment_date, datetime.min.time())
            end_datetime = datetime.combine(appointment_date, datetime.max.time())
            
            appointments = db.query(Appointment).filter(
                Appointment.date >= start_datetime,
                Appointment.date <= end_datetime,
                Appointment.status == "scheduled"
            ).all()
            
            return [
                {
                    "id": apt.id,
                    "vehicle_id": apt.vehicle_id,
                    "service_type": apt.service_type,
                    "time": apt.time,
                    "date": apt.date.isoformat()
                }
                for apt in appointments
            ]
        finally:
            db.close()
    
    async def get_upcoming_appointments(self, vehicle_id: str) -> List[Dict[str, Any]]:
        """Get upcoming appointments for a vehicle"""
        db = self.get_db_session()
        try:
            appointments = db.query(Appointment).filter(
                Appointment.vehicle_id == vehicle_id,
                Appointment.date >= datetime.utcnow(),
                Appointment.status == "scheduled"
            ).order_by(Appointment.date).all()
            
            return [
                {
                    "id": apt.id,
                    "service_type": apt.service_type,
                    "date": apt.date.isoformat(),
                    "time": apt.time,
                    "status": apt.status
                }
                for apt in appointments
            ]
        finally:
            db.close()
    
    async def cancel_appointment(self, appointment_id: str):
        """Cancel an appointment"""
        db = self.get_db_session()
        try:
            appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if appointment:
                appointment.status = "cancelled"
                db.commit()
        finally:
            db.close()
    
    async def store_alert(self, vehicle_id: str, alert_data: Dict[str, Any]):
        """Store alert"""
        db = self.get_db_session()
        try:
            alert = Alert(
                id=str(uuid.uuid4()),
                vehicle_id=vehicle_id,
                message=alert_data["message"],
                level=alert_data.get("level", "info"),
                recommended_service=alert_data.get("recommended_service"),
                health_scores=alert_data.get("health_scores", {})
            )
            db.add(alert)
            db.commit()
        finally:
            db.close()
    
    async def store_conversation(self, session_id: str, message: str, response: str):
        """Store conversation"""
        db = self.get_db_session()
        try:
            conversation = Conversation(
                id=str(uuid.uuid4()),
                session_id=session_id,
                message=message,
                response=response
            )
            db.add(conversation)
            db.commit()
        finally:
            db.close()
    
    async def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history"""
        db = self.get_db_session()
        try:
            conversations = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).order_by(Conversation.created_at).all()
            
            return [
                {
                    "message": conv.message,
                    "response": conv.response,
                    "timestamp": conv.created_at.isoformat()
                }
                for conv in conversations
            ]
        finally:
            db.close()
    
    async def store_feedback(self, feedback_data: Dict[str, Any]):
        """Store feedback"""
        db = self.get_db_session()
        try:
            feedback = Feedback(
                id=str(uuid.uuid4()),
                vehicle_id=feedback_data["vehicle_id"],
                service_id=feedback_data["service_id"],
                rating=feedback_data.get("rating", 0),
                comments=feedback_data.get("comments", ""),
                service_quality=feedback_data.get("service_quality", {})
            )
            db.add(feedback)
            db.commit()
        finally:
            db.close()
    
    async def store_manufacturing_feedback(self, vehicle_id: str, service_id: str, insights: Dict[str, Any]):
        """Store manufacturing feedback"""
        document = {
            "vehicle_id": vehicle_id,
            "service_id": service_id,
            "insights": insights,
            "timestamp": datetime.utcnow()
        }
        mongo_db.manufacturing_feedback.insert_one(document)
    
    async def get_feedback_summary(self, vehicle_id: str) -> Dict[str, Any]:
        """Get feedback summary for a vehicle"""
        db = self.get_db_session()
        try:
            feedbacks = db.query(Feedback).filter(
                Feedback.vehicle_id == vehicle_id
            ).all()
            
            if not feedbacks:
                return {
                    "average_rating": 0,
                    "total_feedback": 0,
                    "feedbacks": []
                }
            
            ratings = [f.rating for f in feedbacks]
            return {
                "average_rating": sum(ratings) / len(ratings),
                "total_feedback": len(feedbacks),
                "feedbacks": [
                    {
                        "id": f.id,
                        "rating": f.rating,
                        "comments": f.comments,
                        "created_at": f.created_at.isoformat()
                    }
                    for f in feedbacks
                ]
            }
        finally:
            db.close()

