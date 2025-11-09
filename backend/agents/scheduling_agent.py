"""
Scheduling Agent - Manages maintenance appointments
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger

from services.database_service import DatabaseService


class SchedulingAgent:
    """
    Agent responsible for scheduling maintenance appointments
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        # Available time slots (9 AM to 5 PM, every hour)
        self.available_slots = list(range(9, 17))
        
    async def schedule_appointment(self, vehicle_id: str, service_type: str, preferred_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Schedule a maintenance appointment
        
        Args:
            vehicle_id: Vehicle identifier
            service_type: Type of service
            preferred_date: Preferred date (ISO format)
            
        Returns:
            Scheduling result
        """
        try:
            logger.info(f"📅 Scheduling Agent: Scheduling {service_type} for vehicle {vehicle_id}")
            
            # Parse preferred date or use default (next available slot)
            if preferred_date:
                try:
                    appointment_date = datetime.fromisoformat(preferred_date)
                except:
                    appointment_date = datetime.now() + timedelta(days=1)
            else:
                appointment_date = datetime.now() + timedelta(days=1)
            
            # Find available slot
            available_slot = await self._find_available_slot(appointment_date)
            
            if not available_slot:
                # Try next day
                appointment_date = appointment_date + timedelta(days=1)
                available_slot = await self._find_available_slot(appointment_date)
            
            if not available_slot:
                return {
                    "status": "error",
                    "message": "No available slots found. Please try a different date."
                }
            
            # Create appointment
            appointment = {
                "vehicle_id": vehicle_id,
                "service_type": service_type,
                "date": available_slot["date"].isoformat(),
                "time": available_slot["time"],
                "status": "scheduled",
                "estimated_duration": self._get_service_duration(service_type),
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Store appointment
            await self.db_service.store_appointment(appointment)
            
            return {
                "status": "scheduled",
                "appointment": appointment,
                "message": f"Appointment scheduled for {available_slot['date'].strftime('%Y-%m-%d')} at {available_slot['time']}:00"
            }
            
        except Exception as e:
            logger.error(f"❌ Scheduling Agent error: {e}")
            raise
    
    async def auto_schedule(self, vehicle_id: str, service_type: str) -> Dict[str, Any]:
        """
        Automatically schedule an appointment for critical issues
        
        Args:
            vehicle_id: Vehicle identifier
            service_type: Type of service
            
        Returns:
            Scheduling result
        """
        # Auto-schedule for next available slot (prioritize sooner dates)
        preferred_date = (datetime.now() + timedelta(days=1)).isoformat()
        return await self.schedule_appointment(vehicle_id, service_type, preferred_date)
    
    async def _find_available_slot(self, date: datetime) -> Optional[Dict[str, Any]]:
        """
        Find available time slot for a given date
        
        Args:
            date: Date to check
            
        Returns:
            Available slot or None
        """
        # Check existing appointments for this date
        existing_appointments = await self.db_service.get_appointments_by_date(date.date())
        booked_times = [apt.get("time") for apt in existing_appointments]
        
        # Find first available slot
        for slot in self.available_slots:
            if slot not in booked_times:
                return {
                    "date": date,
                    "time": slot
                }
        
        return None
    
    def _get_service_duration(self, service_type: str) -> int:
        """
        Get estimated duration for a service type (in minutes)
        
        Args:
            service_type: Type of service
            
        Returns:
            Duration in minutes
        """
        durations = {
            "battery_replacement": 60,
            "brake_replacement": 120,
            "oil_change": 30,
            "engine_inspection": 90,
            "general_inspection": 60,
            "diagnostic_check": 45,
            "tire_rotation": 30,
            "tire_replacement": 60
        }
        
        return durations.get(service_type, 60)
    
    async def get_available_slots(self, date: str) -> List[Dict[str, Any]]:
        """
        Get available time slots for a given date
        
        Args:
            date: Date in ISO format
            
        Returns:
            List of available slots
        """
        try:
            appointment_date = datetime.fromisoformat(date)
            existing_appointments = await self.db_service.get_appointments_by_date(appointment_date.date())
            booked_times = [apt.get("time") for apt in existing_appointments]
            
            available_slots = []
            for slot in self.available_slots:
                if slot not in booked_times:
                    available_slots.append({
                        "time": slot,
                        "available": True
                    })
                else:
                    available_slots.append({
                        "time": slot,
                        "available": False
                    })
            
            return available_slots
            
        except Exception as e:
            logger.error(f"Error getting available slots: {e}")
            return []
    
    async def get_upcoming_appointments(self, vehicle_id: str) -> List[Dict[str, Any]]:
        """
        Get upcoming appointments for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            List of upcoming appointments
        """
        return await self.db_service.get_upcoming_appointments(vehicle_id)
    
    async def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """
        Cancel an appointment
        
        Args:
            appointment_id: Appointment identifier
            
        Returns:
            Cancellation result
        """
        try:
            await self.db_service.cancel_appointment(appointment_id)
            return {
                "status": "cancelled",
                "appointment_id": appointment_id
            }
        except Exception as e:
            logger.error(f"Error cancelling appointment: {e}")
            raise

