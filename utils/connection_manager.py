"""
    Module: connection_manager.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
from typing import List

from fastapi import WebSocket


class ConnectionManager:
    ALLOW_MULTI_CONNECTION = False

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) == 0:
            await websocket.accept()
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

