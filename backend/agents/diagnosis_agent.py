"""
Diagnosis Agent - Predicts component failures using ML models
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from loguru import logger

from models.failure_predictor import FailurePredictor
from services.database_service import DatabaseService


class DiagnosisAgent:
    """
    Agent responsible for predicting component failures
    """
    
    def __init__(self):
        self.failure_predictor = FailurePredictor()
        self.db_service = DatabaseService()
        
    async def predict_failures(self, vehicle_id: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict potential component failures
        
        Args:
            vehicle_id: Vehicle identifier
            analysis_result: Analysis result from Data Analysis Agent
            
        Returns:
            Failure predictions with recommendations
        """
        try:
            logger.info(f"🔬 Diagnosis Agent: Predicting failures for vehicle {vehicle_id}")
            
            metrics = analysis_result.get("metrics", {})
            health_scores = analysis_result.get("health_scores", {})
            anomalies = analysis_result.get("anomalies", [])
            
            # Predict failures using ML model
            predictions = self.failure_predictor.predict(metrics, health_scores)
            
            # Determine criticality
            critical_alert = False
            auto_schedule = False
            recommended_service = None
            alert_level = "info"
            
            # Check for critical issues
            if health_scores.get("battery", 100) < 30:
                critical_alert = True
                auto_schedule = True
                recommended_service = "battery_replacement"
                alert_level = "critical"
            elif health_scores.get("engine", 100) < 40:
                critical_alert = True
                auto_schedule = True
                recommended_service = "engine_inspection"
                alert_level = "critical"
            elif health_scores.get("brakes", 100) < 30:
                critical_alert = True
                auto_schedule = True
                recommended_service = "brake_replacement"
                alert_level = "critical"
            elif health_scores.get("oil", 100) < 40:
                critical_alert = True
                auto_schedule = False
                recommended_service = "oil_change"
                alert_level = "warning"
            elif health_scores.get("overall", 100) < 50:
                critical_alert = True
                auto_schedule = False
                recommended_service = "general_inspection"
                alert_level = "warning"
            elif len(anomalies) > 0:
                critical_alert = True
                auto_schedule = False
                recommended_service = "diagnostic_check"
                alert_level = "warning"
            
            # Get predicted failure timeline
            failure_timeline = self._calculate_failure_timeline(predictions, health_scores)
            
            result = {
                "vehicle_id": vehicle_id,
                "predictions": predictions,
                "failure_timeline": failure_timeline,
                "critical_alert": critical_alert,
                "alert_level": alert_level,
                "auto_schedule": auto_schedule,
                "recommended_service": recommended_service,
                "health_scores": health_scores,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store predictions
            await self.db_service.store_predictions(vehicle_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Diagnosis Agent error: {e}")
            raise
    
    def _calculate_failure_timeline(self, predictions: Dict[str, Any], health_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate predicted failure timeline
        
        Args:
            predictions: ML model predictions
            health_scores: Component health scores
            
        Returns:
            Failure timeline for each component
        """
        timeline = {}
        
        for component, score in health_scores.items():
            if component == "overall":
                continue
                
            if score >= 80:
                timeline[component] = {
                    "days_until_failure": None,
                    "status": "healthy",
                    "confidence": "high"
                }
            elif score >= 50:
                # Estimate days based on degradation rate
                degradation_rate = (100 - score) / 100
                estimated_days = int(180 * degradation_rate)  # Rough estimate
                timeline[component] = {
                    "days_until_failure": estimated_days,
                    "status": "monitor",
                    "confidence": "medium"
                }
            elif score >= 30:
                estimated_days = int(30 * (score / 30))
                timeline[component] = {
                    "days_until_failure": estimated_days,
                    "status": "warning",
                    "confidence": "high"
                }
            else:
                timeline[component] = {
                    "days_until_failure": 0,
                    "status": "critical",
                    "confidence": "high",
                    "immediate_action_required": True
                }
        
        return timeline
    
    async def get_predictions(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Get latest predictions for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Latest predictions
        """
        return await self.db_service.get_latest_predictions(vehicle_id)

