"""
    Module: server.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
import uvicorn
from fastapi import FastAPI

from routes import websocket_routes, camera_routes
from utils.camera_states import State
from utils.connection_manager import ConnectionManager
from utils.baslor_cam import Cam

app = FastAPI()

manager = ConnectionManager()
app.websocket_manager = manager
app.camera = Cam()
app.camera_state = State.OFFLINE

app.include_router(websocket_routes.router)
app.include_router(camera_routes.router)

if __name__ == '__main__':
    uvicorn.run(app)