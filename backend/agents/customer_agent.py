"""
Customer Agent - Handles customer interactions via chatbot/voice
"""
from typing import Dict, List, Any
import os
from loguru import logger

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available. Using rule-based responses.")

from services.database_service import DatabaseService
class CustomerAgent:
    """
    Agent responsible for customer communication
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
            except Exception:
                self.openai_client = None
        else:
            self.openai_client = None
        
    async def process_message(self, message: str, session_id: str) -> str:
        """
        Process customer message and generate response
        
        Args:
            message: Customer message
            session_id: Session identifier
            
        Returns:
            Agent response
        """
        try:
            logger.info(f"💬 Customer Agent: Processing message from session {session_id}")
            
            # Get conversation history
            history = await self.db_service.get_conversation_history(session_id)
            
            # Prepare context
            context = self._prepare_context(session_id, history)
            
            # Generate response using OpenAI
            response = await self._generate_response(message, context, history)
            
            # Store conversation
            await self.db_service.store_conversation(session_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Customer Agent error: {e}")
            # Fallback response
            return "I apologize, but I'm experiencing technical difficulties. Please try again later or contact our support team."
    
    async def _generate_response(self, message: str, context: str, history: List[Dict]) -> str:
        """
        Generate response using OpenAI GPT
        
        Args:
            message: Customer message
            context: Context about vehicle and services
            history: Conversation history
            
        Returns:
            Generated response
        """
        if not self.openai_client:
            # Fallback to rule-based if OpenAI is not configured
            return self._fallback_response(message)
        
        try:
            # Prepare messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a helpful vehicle maintenance assistant. You help customers with:
- Vehicle health and diagnostics
- Scheduling maintenance appointments
- Answering questions about their vehicle
- Providing maintenance recommendations

Context: {context}

Be friendly, professional, and concise. If you don't know something, ask for more information or suggest contacting support."""
                }
            ]
            
            # Add conversation history
            for h in history[-5:]:  # Last 5 messages
                messages.append({"role": "user", "content": h.get("message", "")})
                messages.append({"role": "assistant", "content": h.get("response", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to rule-based responses
            return self._fallback_response(message)
    
    def _prepare_context(self, session_id: str, history: List[Dict]) -> str:
        """
        Prepare context for the AI model
        
        Args:
            session_id: Session identifier
            history: Conversation history
            
        Returns:
            Context string
        """
        # In a real implementation, fetch vehicle data and recent alerts
        context = f"""
Session ID: {session_id}
Recent alerts: None
Upcoming appointments: None
Vehicle status: Normal
"""
        return context
    
    def _fallback_response(self, message: str) -> str:
        """
        Fallback response when OpenAI is unavailable
        
        Args:
            message: Customer message
            
        Returns:
            Fallback response
        """
        message_lower = message.lower()
        
        if "schedule" in message_lower or "appointment" in message_lower:
            return "I can help you schedule a maintenance appointment. Please provide your vehicle ID and preferred date."
        elif "battery" in message_lower:
            return "I can check your battery status. Let me retrieve that information for you."
        elif "brake" in message_lower:
            return "I can help with brake-related questions. Would you like me to check your brake pad status?"
        elif "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm your vehicle maintenance assistant. How can I help you today?"
        else:
            return "I understand you're asking about your vehicle. Let me help you with that. Could you provide more details?"
    
    async def send_alert(self, vehicle_id: str, diagnosis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send alert to customer about critical issues
        
        Args:
            vehicle_id: Vehicle identifier
            diagnosis_result: Diagnosis result with alerts
            
        Returns:
            Alert sending result
        """
        try:
            logger.info(f"📢 Customer Agent: Sending alert for vehicle {vehicle_id}")
            
            alert_level = diagnosis_result.get("alert_level", "info")
            recommended_service = diagnosis_result.get("recommended_service", "inspection")
            health_scores = diagnosis_result.get("health_scores", {})
            
            # Create alert message
            if alert_level == "critical":
                message = f"🚨 CRITICAL ALERT: Your vehicle {vehicle_id} requires immediate attention. Recommended service: {recommended_service}"
            else:
                message = f"⚠️ WARNING: Your vehicle {vehicle_id} needs maintenance. Recommended service: {recommended_service}"
            
            # Store alert
            await self.db_service.store_alert(vehicle_id, {
                "message": message,
                "level": alert_level,
                "recommended_service": recommended_service,
                "health_scores": health_scores
            })
            
            # In a real implementation, send via SMS, email, or push notification
            return {
                "status": "sent",
                "vehicle_id": vehicle_id,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"❌ Customer Agent alert error: {e}")
            raise

