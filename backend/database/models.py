"""
SQLAlchemy database models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from database.connection import Base


class Vehicle(Base):
    """Vehicle model"""
    __tablename__ = "vehicles"
    
    id = Column(String, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    vin = Column(String, unique=True)
    owner_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"
    
    id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    service_type = Column(String)
    date = Column(DateTime(timezone=True))
    time = Column(Integer)  # Hour of day (0-23)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    estimated_duration = Column(Integer)  # Duration in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Feedback(Base):
    """Feedback model"""
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    service_id = Column(String, index=True)
    rating = Column(Integer)  # 1-5
    comments = Column(Text)
    service_quality = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    """Alert model"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    message = Column(Text)
    level = Column(String)  # info, warning, critical
    recommended_service = Column(String)
    health_scores = Column(JSON)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

