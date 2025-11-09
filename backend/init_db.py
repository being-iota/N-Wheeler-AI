"""
Database initialization script
"""
import asyncio
from database.connection import init_db, Base, engine


async def main():
    """Initialize database tables"""
    print("🔄 Initializing database...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

