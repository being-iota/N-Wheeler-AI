"""
API routes for the vehicle maintenance system
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.master_agent import MasterAgent
from services.database_service import DatabaseService
from services.telematics_simulator import TelematicsSimulator
from ueba.monitor import UEBAMonitor

router = APIRouter()
master_agent = MasterAgent()
db_service = DatabaseService()
telematics_simulator = TelematicsSimulator()
ueba_monitor = UEBAMonitor()


# Pydantic models
class TelematicsData(BaseModel):
    vehicle_id: str
    battery_voltage: float
    engine_temp: float
    oil_pressure: float
    brake_pad_thickness: float
    tire_pressure: float
    mileage: float
    rpm: float
    speed: float
    timestamp: Optional[str] = None


class CustomerMessage(BaseModel):
    message: str
    session_id: str


class ScheduleRequest(BaseModel):
    vehicle_id: str
    service_type: str
    preferred_date: Optional[str] = None


class FeedbackRequest(BaseModel):
    vehicle_id: str
    service_id: str
    rating: int
    comments: Optional[str] = None
    service_quality: Optional[Dict[str, Any]] = None


@router.post("/telematics")
async def receive_telematics_data(data: TelematicsData):
    """Receive and process telematics data"""
    try:
        sensor_data = data.dict()
        result = await master_agent.process_telematics_data(data.vehicle_id, sensor_data)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles/{vehicle_id}/status")
async def get_vehicle_status(vehicle_id: str):
    """Get comprehensive vehicle status"""
    try:
        status = await master_agent.get_vehicle_status(vehicle_id)
        return {"status": "success", "data": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat_with_customer(message: CustomerMessage):
    """Chat with customer via chatbot"""
    try:
        response = await master_agent.handle_customer_query(message.session_id, message.message)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule")
async def schedule_maintenance(request: ScheduleRequest):
    """Schedule maintenance appointment"""
    try:
        result = await master_agent.schedule_maintenance(
            request.vehicle_id,
            request.service_type,
            request.preferred_date
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/available-slots")
async def get_available_slots(date: str):
    """Get available time slots for a date"""
    try:
        from agents.scheduling_agent import SchedulingAgent
        scheduling_agent = SchedulingAgent()
        slots = await scheduling_agent.get_available_slots(date)
        return {"status": "success", "slots": slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit service feedback"""
    try:
        feedback_data = {
            "rating": feedback.rating,
            "comments": feedback.comments,
            "service_quality": feedback.service_quality or {}
        }
        result = await master_agent.submit_feedback(
            feedback.vehicle_id,
            feedback.service_id,
            feedback_data
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles/{vehicle_id}/alerts")
async def get_alerts(vehicle_id: str):
    """Get alerts for a vehicle"""
    try:
        # This would query the database for alerts
        alerts = await db_service.get_upcoming_appointments(vehicle_id)  # Placeholder
        return {"status": "success", "alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles")
async def get_all_vehicles():
    """Get all vehicles with telematics data"""
    try:
        vehicles = telematics_simulator.get_all_vehicles()
        return {"status": "success", "vehicles": vehicles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ueba/activity")
async def get_ueba_activity(agent_name: Optional[str] = None):
    """Get UEBA activity summary"""
    try:
        summary = ueba_monitor.get_activity_summary(agent_name)
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

