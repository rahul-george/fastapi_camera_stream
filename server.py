"""
    Module: server.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
import uvicorn
from fastapi import FastAPI

from routes.websocket_routes import router
from utils.connection_manager import ConnectionManager
from utils.baslor_cam import Cam

app = FastAPI()

manager = ConnectionManager()
app.websocket_manager = manager
app.camera = Cam()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app)