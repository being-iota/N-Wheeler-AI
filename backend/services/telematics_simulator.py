"""
Telematics data simulator for testing
"""
import asyncio
import random
import time
from typing import Dict, Any, Optional
from datetime import datetime
from threading import Thread


class TelematicsSimulator:
    """
    Simulates real-time telematics data from vehicles
    """
    
    def __init__(self):
        self.running = False
        self.vehicles = {}
        self.thread = None
        
        # Initialize some demo vehicles
        self.vehicles = {
            "VEH001": {
                "battery_voltage": 12.6,
                "engine_temp": 90.0,
                "oil_pressure": 50.0,
                "brake_pad_thickness": 8.0,
                "tire_pressure": 32.0,
                "mileage": 45000,
                "rpm": 2000,
                "speed": 60
            },
            "VEH002": {
                "battery_voltage": 11.5,  # Low battery
                "engine_temp": 95.0,
                "oil_pressure": 45.0,
                "brake_pad_thickness": 2.5,  # Low brake pads
                "tire_pressure": 31.0,
                "mileage": 120000,
                "rpm": 2500,
                "speed": 70
            },
            "VEH003": {
                "battery_voltage": 12.8,
                "engine_temp": 88.0,
                "oil_pressure": 52.0,
                "brake_pad_thickness": 10.0,
                "tire_pressure": 32.0,
                "mileage": 25000,
                "rpm": 1800,
                "speed": 55
            }
        }
    
    def start(self):
        """Start the simulator"""
        if not self.running:
            self.running = True
            self.thread = Thread(target=self._simulate_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the simulator"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _simulate_loop(self):
        """Main simulation loop"""
        while self.running:
            for vehicle_id, data in self.vehicles.items():
                # Simulate gradual changes in sensor values
                data["battery_voltage"] += random.uniform(-0.05, 0.05)
                data["battery_voltage"] = max(11.0, min(13.0, data["battery_voltage"]))
                
                data["engine_temp"] += random.uniform(-2, 2)
                data["engine_temp"] = max(80, min(115, data["engine_temp"]))
                
                data["oil_pressure"] += random.uniform(-1, 1)
                data["oil_pressure"] = max(35, min(65, data["oil_pressure"]))
                
                # Brake pads gradually wear down
                if random.random() < 0.1:  # 10% chance of wear
                    data["brake_pad_thickness"] -= random.uniform(0, 0.01)
                    data["brake_pad_thickness"] = max(0, data["brake_pad_thickness"])
                
                data["tire_pressure"] += random.uniform(-0.5, 0.5)
                data["tire_pressure"] = max(28, min(36, data["tire_pressure"]))
                
                data["rpm"] = random.randint(1000, 3000)
                data["speed"] = random.randint(0, 80)
                
                # Add timestamp
                data["timestamp"] = datetime.utcnow().isoformat()
            
            time.sleep(5)  # Update every 5 seconds
    
    def get_latest_data(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """Get latest data for a vehicle"""
        if vehicle_id in self.vehicles:
            return {
                "vehicle_id": vehicle_id,
                **self.vehicles[vehicle_id]
            }
        return None
    
    def get_all_vehicles(self) -> Dict[str, Dict[str, Any]]:
        """Get all vehicle data"""
        return self.vehicles.copy()

