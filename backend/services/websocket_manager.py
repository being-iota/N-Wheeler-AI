"""
WebSocket connection manager
"""
from fastapi import WebSocket
from typing import Dict, List
import json


class WebSocketManager:
    """
    Manages WebSocket connections
    """
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
    
    def disconnect(self, client_id: str):
        """Remove WebSocket connection"""
        if client_id in self.active_connections:
            self.active_connections[client_id] = [
                ws for ws in self.active_connections[client_id]
                if ws.client_state.name != "DISCONNECTED"
            ]
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
    
    async def send_personal_message(self, message: dict, client_id: str):
        """Send message to specific client"""
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def broadcast(self, message: dict, client_ids: List[str] = None):
        """Broadcast message to all or specific clients"""
        if client_ids is None:
            client_ids = list(self.active_connections.keys())
        
        for client_id in client_ids:
            await self.send_personal_message(message, client_id)

