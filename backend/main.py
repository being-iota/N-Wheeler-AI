"""
Main FastAPI application for Multi-Agent Vehicle Maintenance System
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import List
import asyncio
from loguru import logger

from api import routes
from services.websocket_manager import WebSocketManager
from services.telematics_simulator import TelematicsSimulator
from database.connection import init_db
from ueba.monitor import UEBAMonitor


# WebSocket manager instance
ws_manager = WebSocketManager()
telematics_simulator = TelematicsSimulator()
ueba_monitor = UEBAMonitor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on startup/shutdown"""
    # Startup
    print("🚀 Starting Vehicle Maintenance System...")
    await init_db()
    telematics_simulator.start()
    ueba_monitor.start_monitoring()
    print("✅ System initialized successfully")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    telematics_simulator.stop()
    ueba_monitor.stop_monitoring()
    print("✅ Shutdown complete")


app = FastAPI(
    title="N-Wheeler AI",
    description="Intelligent Vehicle Maintenance System with Multi-Agent AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "N-Wheeler AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "telematics": "running"
        }
    }


@app.websocket("/ws/telematics/{vehicle_id}")
async def websocket_telematics(websocket: WebSocket, vehicle_id: str):
    """WebSocket endpoint for real-time telematics data"""
    await ws_manager.connect(websocket, vehicle_id)
    try:
        while True:
            # Send telematics data to client
            data = telematics_simulator.get_latest_data(vehicle_id)
            if data:
                await websocket.send_json(data)
            await asyncio.sleep(1)  # Send data every second
    except WebSocketDisconnect:
        ws_manager.disconnect(vehicle_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(vehicle_id)


@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for chatbot communication"""
    await ws_manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Process chat message through customer agent
            from agents.customer_agent import CustomerAgent
            customer_agent = CustomerAgent()
            response = await customer_agent.process_message(data.get("message", ""), session_id)
            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"Chat WebSocket error: {e}")
        ws_manager.disconnect(session_id)


if __name__ == "__main__":
    import asyncio
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

