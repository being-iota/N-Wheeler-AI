"""
Feedback Agent - Collects and processes service feedback
"""
from typing import Dict, List, Any
from datetime import datetime
from loguru import logger

from services.database_service import DatabaseService


class FeedbackAgent:
    """
    Agent responsible for collecting and processing service feedback
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        
    async def process_feedback(self, vehicle_id: str, service_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process service feedback
        
        Args:
            vehicle_id: Vehicle identifier
            service_id: Service appointment ID
            feedback_data: Feedback data (rating, comments, etc.)
            
        Returns:
            Feedback processing result
        """
        try:
            logger.info(f"📝 Feedback Agent: Processing feedback for service {service_id}")
            
            # Extract feedback data
            rating = feedback_data.get("rating", 0)
            comments = feedback_data.get("comments", "")
            service_quality = feedback_data.get("service_quality", {})
            
            # Store feedback
            feedback = {
                "vehicle_id": vehicle_id,
                "service_id": service_id,
                "rating": rating,
                "comments": comments,
                "service_quality": service_quality,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.db_service.store_feedback(feedback)
            
            # Analyze feedback for manufacturing
            manufacturing_insights = await self._analyze_for_manufacturing(feedback)
            
            # Send to manufacturing (in real implementation, this would be an API call)
            await self._send_to_manufacturing(vehicle_id, service_id, manufacturing_insights)
            
            return {
                "status": "processed",
                "feedback": feedback,
                "manufacturing_insights": manufacturing_insights
            }
            
        except Exception as e:
            logger.error(f"❌ Feedback Agent error: {e}")
            raise
    
    async def _analyze_for_manufacturing(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze feedback for manufacturing insights
        
        Args:
            feedback: Feedback data
            
        Returns:
            Manufacturing insights
        """
        rating = feedback.get("rating", 0)
        comments = feedback.get("comments", "").lower()
        service_quality = feedback.get("service_quality", {})
        
        insights = {
            "rating": rating,
            "sentiment": "positive" if rating >= 4 else "negative" if rating <= 2 else "neutral",
            "keywords": [],
            "issues": [],
            "recommendations": []
        }
        
        # Extract keywords from comments
        if "defect" in comments or "faulty" in comments:
            insights["keywords"].append("defect")
            insights["issues"].append("Potential manufacturing defect reported")
        
        if "quality" in comments:
            insights["keywords"].append("quality")
        
        if "excellent" in comments or "great" in comments:
            insights["keywords"].append("positive_feedback")
        
        # Analyze service quality metrics
        if service_quality:
            if service_quality.get("component_quality", 0) < 3:
                insights["issues"].append("Component quality concerns")
                insights["recommendations"].append("Review component quality standards")
        
        return insights
    
    async def _send_to_manufacturing(self, vehicle_id: str, service_id: str, insights: Dict[str, Any]) -> None:
        """
        Send feedback insights to manufacturing system
        
        Args:
            vehicle_id: Vehicle identifier
            service_id: Service appointment ID
            insights: Manufacturing insights
            
        Returns:
            None
        """
        # In a real implementation, this would be an API call to manufacturing system
        logger.info(f"📤 Feedback Agent: Sending insights to manufacturing for vehicle {vehicle_id}")
        logger.info(f"Manufacturing insights: {insights}")
        
        # Store for manufacturing review
        await self.db_service.store_manufacturing_feedback(vehicle_id, service_id, insights)
    
    async def get_feedback_summary(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Get feedback summary for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Feedback summary
        """
        return await self.db_service.get_feedback_summary(vehicle_id)

