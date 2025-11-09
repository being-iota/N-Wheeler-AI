"""
UEBA Monitor - Detects anomalous agent behavior
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict
from loguru import logger
import numpy as np
import joblib
import os

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available for UEBA. Using rule-based monitoring.")


class UEBAMonitor:
    """
    Monitors agent behavior and detects anomalies
    """
    
    def __init__(self):
        self.activity_logs = []
        self.model_path = "./models/ueba_model.pkl"
        self.model = None
        self.agent_activity_counts = defaultdict(int)
        self._load_or_create_model()
        
        # Normal behavior patterns
        self.normal_patterns = {
            "master_agent": {
                "max_calls_per_minute": 100,
                "allowed_actions": ["process_telematics_data", "handle_customer_query", "schedule_maintenance", "submit_feedback", "get_vehicle_status"]
            },
            "data_analysis_agent": {
                "max_calls_per_minute": 200,
                "allowed_actions": ["analyze_data", "get_latest_analysis"]
            },
            "diagnosis_agent": {
                "max_calls_per_minute": 100,
                "allowed_actions": ["predict_failures", "get_predictions"]
            },
            "customer_agent": {
                "max_calls_per_minute": 50,
                "allowed_actions": ["process_message", "send_alert"]
            },
            "scheduling_agent": {
                "max_calls_per_minute": 30,
                "allowed_actions": ["schedule_appointment", "auto_schedule", "get_available_slots", "cancel_appointment"]
            },
            "feedback_agent": {
                "max_calls_per_minute": 20,
                "allowed_actions": ["process_feedback", "get_feedback_summary"]
            }
        }
    
    def _load_or_create_model(self):
        """Load or create UEBA model"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except:
                self.model = self._create_model()
        else:
            self.model = self._create_model()
    
    def _create_model(self):
        """Create Isolation Forest model for UEBA"""
        if not SKLEARN_AVAILABLE:
            return None  # Return None if sklearn is not available
        
        model = IsolationForest(contamination=0.05, random_state=42)
        
        # Train on synthetic normal behavior data
        training_data = self._generate_training_data()
        model.fit(training_data)
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)
        
        return model
    
    def _generate_training_data(self):
        """Generate synthetic training data for normal behavior"""
        n_samples = 500
        data = []
        
        for _ in range(n_samples):
            # Normal features: agent_id (encoded), action_count, time_of_day, etc.
            sample = [
                np.random.randint(0, 6),  # Agent ID (0-5)
                np.random.randint(1, 50),  # Actions per hour
                np.random.randint(0, 24),  # Hour of day
                np.random.randint(0, 7),   # Day of week
                np.random.uniform(0, 1)    # Normalized success rate
            ]
            data.append(sample)
        
        return np.array(data)
    
    def start_monitoring(self):
        """Start monitoring agent activities"""
        logger.info("🔒 UEBA Monitor: Started monitoring")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        logger.info("🔒 UEBA Monitor: Stopped monitoring")
    
    def log_agent_activity(self, agent_name: str, action: str, metadata: Dict[str, Any] = None):
        """
        Log agent activity for analysis
        
        Args:
            agent_name: Name of the agent
            action: Action performed
            metadata: Additional metadata
        """
        activity = {
            "agent": agent_name,
            "action": action,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
            "hour": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday()
        }
        
        self.activity_logs.append(activity)
        
        # Keep only last 10000 logs
        if len(self.activity_logs) > 10000:
            self.activity_logs = self.activity_logs[-10000:]
        
        # Check for anomalies
        anomaly = self._check_anomaly(agent_name, action)
        
        if anomaly:
            logger.warning(f"⚠️ UEBA Alert: Anomalous activity detected - Agent: {agent_name}, Action: {action}")
            self._handle_anomaly(activity, anomaly)
        
        # Update activity counts
        key = f"{agent_name}:{action}"
        self.agent_activity_counts[key] += 1
    
    def _check_anomaly(self, agent_name: str, action: str) -> Dict[str, Any]:
        """
        Check if activity is anomalous
        
        Args:
            agent_name: Name of the agent
            action: Action performed
            
        Returns:
            Anomaly details or None
        """
        anomalies = []
        
        # Check 1: Rate limiting
        if agent_name in self.normal_patterns:
            pattern = self.normal_patterns[agent_name]
            recent_activities = [
                log for log in self.activity_logs[-100:]
                if log["agent"] == agent_name
                and (datetime.utcnow() - log["timestamp"]).seconds < 60
            ]
            
            if len(recent_activities) > pattern["max_calls_per_minute"]:
                anomalies.append({
                    "type": "rate_limit_exceeded",
                    "severity": "high",
                    "message": f"Agent {agent_name} exceeded rate limit ({pattern['max_calls_per_minute']} calls/min)"
                })
        
        # Check 2: Unauthorized action
        if agent_name in self.normal_patterns:
            pattern = self.normal_patterns[agent_name]
            if action not in pattern["allowed_actions"]:
                anomalies.append({
                    "type": "unauthorized_action",
                    "severity": "critical",
                    "message": f"Agent {agent_name} attempted unauthorized action: {action}"
                })
        
        # Check 3: ML-based anomaly detection (only if sklearn is available)
        if self.model is not None and SKLEARN_AVAILABLE and len(self.activity_logs) >= 10:
            try:
                features = self._extract_features(agent_name, action)
                if features:
                    prediction = self.model.predict([features])
                    if prediction[0] == -1:
                        anomalies.append({
                            "type": "ml_anomaly",
                            "severity": "medium",
                            "message": f"ML model detected anomalous pattern for agent {agent_name}"
                        })
            except Exception:
                # If ML model fails, skip ML-based detection
                pass
        
        if anomalies:
            return {
                "detected": True,
                "anomalies": anomalies,
                "agent": agent_name,
                "action": action
            }
        
        return None
    
    def _extract_features(self, agent_name: str, action: str) -> List[float]:
        """Extract features for ML model"""
        # Get recent activities for this agent
        recent_activities = [
            log for log in self.activity_logs[-100:]
            if log["agent"] == agent_name
        ]
        
        if len(recent_activities) < 5:
            return None
        
        # Calculate features
        agent_id_map = {
            "master_agent": 0,
            "data_analysis_agent": 1,
            "diagnosis_agent": 2,
            "customer_agent": 3,
            "scheduling_agent": 4,
            "feedback_agent": 5
        }
        
        agent_id = agent_id_map.get(agent_name, 0)
        actions_per_hour = len(recent_activities)
        current_hour = datetime.utcnow().hour
        current_day = datetime.utcnow().weekday()
        success_rate = 1.0  # Assume success for now
        
        return [agent_id, actions_per_hour, current_hour, current_day, success_rate]
    
    def _handle_anomaly(self, activity: Dict[str, Any], anomaly: Dict[str, Any]):
        """Handle detected anomaly"""
        # Log anomaly
        logger.error(f"🚨 UEBA Security Alert: {anomaly}")
        
        # In a real implementation, this would:
        # - Send alert to security team
        # - Block suspicious activity
        # - Generate security report
        # - Store in security log
        
        # For now, just log it
        security_log = {
            "activity": activity,
            "anomaly": anomaly,
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "logged"
        }
        
        # Store in security log (in real implementation, use dedicated security database)
        logger.info(f"Security log: {security_log}")
    
    def get_activity_summary(self, agent_name: str = None) -> Dict[str, Any]:
        """Get activity summary"""
        if agent_name:
            activities = [log for log in self.activity_logs if log["agent"] == agent_name]
        else:
            activities = self.activity_logs
        
        if not activities:
            return {"total_activities": 0}
        
        # Group by agent
        by_agent = defaultdict(int)
        by_action = defaultdict(int)
        
        for activity in activities:
            by_agent[activity["agent"]] += 1
            by_action[f"{activity['agent']}:{activity['action']}"] += 1
        
        return {
            "total_activities": len(activities),
            "by_agent": dict(by_agent),
            "by_action": dict(by_action),
            "recent_activities": [
                {
                    "agent": a["agent"],
                    "action": a["action"],
                    "timestamp": a["timestamp"].isoformat()
                }
                for a in activities[-10:]
            ]
        }

