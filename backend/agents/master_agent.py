"""
Master Agent - Orchestrates all other agents
"""
from typing import Dict, List, Any
import asyncio
from loguru import logger

from agents.data_analysis_agent import DataAnalysisAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.customer_agent import CustomerAgent
from agents.scheduling_agent import SchedulingAgent
from agents.feedback_agent import FeedbackAgent
from ueba.monitor import UEBAMonitor


class MasterAgent:
    """
    Master Agent that coordinates all other agents in the system
    """
    
    def __init__(self):
        self.data_analysis_agent = DataAnalysisAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.customer_agent = CustomerAgent()
        self.scheduling_agent = SchedulingAgent()
        self.feedback_agent = FeedbackAgent()
        self.ueba_monitor = UEBAMonitor()
        
    async def process_telematics_data(self, vehicle_id: str, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming telematics data through the agent pipeline
        
        Args:
            vehicle_id: Vehicle identifier
            sensor_data: Sensor data from vehicle
            
        Returns:
            Processed result with predictions and recommendations
        """
        try:
            # Log agent activity for UEBA
            self.ueba_monitor.log_agent_activity("master_agent", "process_telematics_data", {
                "vehicle_id": vehicle_id
            })
            
            # Step 1: Data Analysis Agent - Analyze sensor data
            logger.info(f"🔍 Master Agent: Analyzing data for vehicle {vehicle_id}")
            analysis_result = await self.data_analysis_agent.analyze_data(vehicle_id, sensor_data)
            
            # Step 2: Diagnosis Agent - Predict failures
            logger.info(f"🔬 Master Agent: Diagnosing potential issues for vehicle {vehicle_id}")
            diagnosis_result = await self.diagnosis_agent.predict_failures(vehicle_id, analysis_result)
            
            # Step 3: Check if immediate action is needed
            if diagnosis_result.get("critical_alert", False):
                logger.warning(f"⚠️ Master Agent: Critical alert for vehicle {vehicle_id}")
                # Step 4: Customer Agent - Notify customer
                await self.customer_agent.send_alert(vehicle_id, diagnosis_result)
                
                # Step 5: Scheduling Agent - Auto-schedule if needed
                if diagnosis_result.get("auto_schedule", False):
                    logger.info(f"📅 Master Agent: Auto-scheduling maintenance for vehicle {vehicle_id}")
                    schedule_result = await self.scheduling_agent.auto_schedule(
                        vehicle_id, 
                        diagnosis_result.get("recommended_service")
                    )
                    diagnosis_result["scheduling"] = schedule_result
            
            return {
                "vehicle_id": vehicle_id,
                "analysis": analysis_result,
                "diagnosis": diagnosis_result,
                "timestamp": sensor_data.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"❌ Master Agent error: {e}")
            raise
    
    async def handle_customer_query(self, session_id: str, message: str) -> str:
        """
        Handle customer query through customer agent
        
        Args:
            session_id: Customer session identifier
            message: Customer message
            
        Returns:
            Agent response
        """
        self.ueba_monitor.log_agent_activity("master_agent", "handle_customer_query", {
            "session_id": session_id
        })
        
        return await self.customer_agent.process_message(message, session_id)
    
    async def schedule_maintenance(self, vehicle_id: str, service_type: str, preferred_date: str = None) -> Dict[str, Any]:
        """
        Schedule maintenance appointment
        
        Args:
            vehicle_id: Vehicle identifier
            service_type: Type of service needed
            preferred_date: Preferred date for service
            
        Returns:
            Scheduling result
        """
        self.ueba_monitor.log_agent_activity("master_agent", "schedule_maintenance", {
            "vehicle_id": vehicle_id,
            "service_type": service_type
        })
        
        return await self.scheduling_agent.schedule_appointment(vehicle_id, service_type, preferred_date)
    
    async def submit_feedback(self, vehicle_id: str, service_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit service feedback
        
        Args:
            vehicle_id: Vehicle identifier
            service_id: Service appointment ID
            feedback_data: Feedback data
            
        Returns:
            Feedback processing result
        """
        self.ueba_monitor.log_agent_activity("master_agent", "submit_feedback", {
            "vehicle_id": vehicle_id,
            "service_id": service_id
        })
        
        return await self.feedback_agent.process_feedback(vehicle_id, service_id, feedback_data)
    
    async def get_vehicle_status(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Get comprehensive vehicle status
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Vehicle status with all agent insights
        """
        self.ueba_monitor.log_agent_activity("master_agent", "get_vehicle_status", {
            "vehicle_id": vehicle_id
        })
        
        # Get latest analysis
        analysis = await self.data_analysis_agent.get_latest_analysis(vehicle_id)
        
        # Get predictions
        predictions = await self.diagnosis_agent.get_predictions(vehicle_id)
        
        # Get scheduled appointments
        appointments = await self.scheduling_agent.get_upcoming_appointments(vehicle_id)
        
        return {
            "vehicle_id": vehicle_id,
            "analysis": analysis,
            "predictions": predictions,
            "appointments": appointments
        }

