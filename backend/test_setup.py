"""
Test script to verify system setup
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pymongo
        import redis
        import sklearn
        import xgboost
        import openai
        import pandas
        import numpy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def test_database_connections():
    """Test database connections"""
    print("\n🔍 Testing database connections...")
    try:
        from database.connection import engine, mongo_client, redis_client
        
        # Test PostgreSQL
        try:
            with engine.connect() as conn:
                print("✅ PostgreSQL connection successful")
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            return False
        
        # Test MongoDB
        try:
            mongo_client.admin.command('ping')
            print("✅ MongoDB connection successful")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
        
        # Test Redis
        try:
            redis_client.ping()
            print("✅ Redis connection successful")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def test_models():
    """Test ML models"""
    print("\n🔍 Testing ML models...")
    try:
        from models.anomaly_detector import AnomalyDetector
        from models.failure_predictor import FailurePredictor
        
        # Test anomaly detector
        detector = AnomalyDetector()
        test_data = {
            "battery_voltage": 12.5,
            "engine_temp": 90.0,
            "oil_pressure": 50.0,
            "brake_pad_thickness": 8.0,
            "tire_pressure": 32.0,
            "rpm": 2000,
            "speed": 60
        }
        anomalies = detector.detect(test_data)
        print(f"✅ Anomaly detector working (detected {len(anomalies)} anomalies)")
        
        # Test failure predictor
        predictor = FailurePredictor()
        metrics = test_data
        health_scores = {"battery": 85, "engine": 90, "brakes": 80, "oil": 85, "tires": 90}
        predictions = predictor.predict(metrics, health_scores)
        print(f"✅ Failure predictor working (predicted {len(predictions)} components)")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_agents():
    """Test agents"""
    print("\n🔍 Testing agents...")
    try:
        from agents.master_agent import MasterAgent
        from agents.data_analysis_agent import DataAnalysisAgent
        from agents.diagnosis_agent import DiagnosisAgent
        from agents.customer_agent import CustomerAgent
        from agents.scheduling_agent import SchedulingAgent
        from agents.feedback_agent import FeedbackAgent
        
        print("✅ All agents imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Vehicle Maintenance AI System - Setup Test\n")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Database Connections", test_database_connections()))
    results.append(("ML Models", test_models()))
    results.append(("Agents", test_agents()))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All tests passed! System is ready to use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

