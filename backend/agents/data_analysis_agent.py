"""
Data Analysis Agent - Processes telematics data and detects anomalies
"""
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from datetime import datetime
from loguru import logger

from models.anomaly_detector import AnomalyDetector
from services.database_service import DatabaseService


class DataAnalysisAgent:
    """
    Agent responsible for analyzing telematics data and detecting anomalies
    """
    
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.db_service = DatabaseService()
        
    async def analyze_data(self, vehicle_id: str, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sensor data and detect anomalies
        
        Args:
            vehicle_id: Vehicle identifier
            sensor_data: Sensor data dictionary
            
        Returns:
            Analysis result with anomalies and metrics
        """
        try:
            logger.info(f"📊 Data Analysis Agent: Analyzing data for vehicle {vehicle_id}")
            
            # Extract metrics
            metrics = {
                "battery_voltage": sensor_data.get("battery_voltage", 12.0),
                "engine_temp": sensor_data.get("engine_temp", 90.0),
                "oil_pressure": sensor_data.get("oil_pressure", 50.0),
                "brake_pad_thickness": sensor_data.get("brake_pad_thickness", 10.0),
                "tire_pressure": sensor_data.get("tire_pressure", 32.0),
                "mileage": sensor_data.get("mileage", 0),
                "rpm": sensor_data.get("rpm", 0),
                "speed": sensor_data.get("speed", 0),
            }
            
            # Detect anomalies
            anomalies = self.anomaly_detector.detect(sensor_data)
            
            # Calculate health scores
            health_scores = self._calculate_health_scores(metrics)
            
            # Store data in database
            await self.db_service.store_telematics_data(vehicle_id, sensor_data, {
                "anomalies": anomalies,
                "health_scores": health_scores
            })
            
            return {
                "vehicle_id": vehicle_id,
                "metrics": metrics,
                "anomalies": anomalies,
                "health_scores": health_scores,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "normal" if len(anomalies) == 0 else "anomaly_detected"
            }
            
        except Exception as e:
            logger.error(f"❌ Data Analysis Agent error: {e}")
            raise
    
    def _calculate_health_scores(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate health scores for various components
        
        Args:
            metrics: Sensor metrics
            
        Returns:
            Health scores (0-100, where 100 is perfect)
        """
        scores = {}
        
        # Battery health (12.6V is optimal, <11.8V is low)
        battery_voltage = metrics.get("battery_voltage", 12.0)
        if battery_voltage >= 12.6:
            scores["battery"] = 100
        elif battery_voltage >= 12.0:
            scores["battery"] = 80 + (battery_voltage - 12.0) * 33.3
        elif battery_voltage >= 11.8:
            scores["battery"] = 50 + (battery_voltage - 11.8) * 250
        else:
            scores["battery"] = max(0, 50 - (11.8 - battery_voltage) * 25)
        
        # Engine health (90°C is optimal, >110°C is overheating)
        engine_temp = metrics.get("engine_temp", 90.0)
        if 85 <= engine_temp <= 95:
            scores["engine"] = 100
        elif 95 < engine_temp <= 110:
            scores["engine"] = 100 - (engine_temp - 95) * 6.67
        elif engine_temp > 110:
            scores["engine"] = max(0, 0 - (engine_temp - 110) * 2)
        else:
            scores["engine"] = max(0, 100 - (85 - engine_temp) * 3)
        
        # Oil pressure health (40-60 PSI is optimal)
        oil_pressure = metrics.get("oil_pressure", 50.0)
        if 40 <= oil_pressure <= 60:
            scores["oil"] = 100
        elif oil_pressure < 40:
            scores["oil"] = max(0, oil_pressure / 40 * 100)
        else:
            scores["oil"] = max(0, 100 - (oil_pressure - 60) * 5)
        
        # Brake pad health (10mm is new, <3mm needs replacement)
        brake_thickness = metrics.get("brake_pad_thickness", 10.0)
        if brake_thickness >= 10:
            scores["brakes"] = 100
        elif brake_thickness >= 3:
            scores["brakes"] = (brake_thickness / 10) * 100
        else:
            scores["brakes"] = max(0, (brake_thickness / 3) * 30)
        
        # Tire pressure health (32 PSI is optimal, ±2 PSI is acceptable)
        tire_pressure = metrics.get("tire_pressure", 32.0)
        if 30 <= tire_pressure <= 34:
            scores["tires"] = 100
        else:
            deviation = abs(tire_pressure - 32)
            scores["tires"] = max(0, 100 - deviation * 10)
        
        # Overall health (weighted average)
        scores["overall"] = (
            scores["battery"] * 0.15 +
            scores["engine"] * 0.25 +
            scores["oil"] * 0.20 +
            scores["brakes"] * 0.25 +
            scores["tires"] * 0.15
        )
        
        return scores
    
    async def get_latest_analysis(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Get latest analysis for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            Latest analysis result
        """
        return await self.db_service.get_latest_analysis(vehicle_id)

