"""
Database connection and initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pymongo import MongoClient
import redis

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/vehicle_maintenance")

try:
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to PostgreSQL: {e}")
    engine = None
    SessionLocal = None

Base = declarative_base()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/telematics")
try:
    mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
    mongo_db = mongo_client.telematics
    # Test connection
    mongo_client.admin.command('ping')
except Exception as e:
    print(f"Warning: Could not connect to MongoDB: {e}")
    mongo_client = None
    mongo_db = None

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    redis_client.ping()
except Exception as e:
    print(f"Warning: Could not connect to Redis: {e}")
    redis_client = None


async def init_db():
    """Initialize database tables"""
    try:
        from database.models import Vehicle, Appointment, Feedback, Alert, Conversation
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

