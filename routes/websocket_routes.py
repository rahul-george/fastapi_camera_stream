"""
    Module: websocket_routes.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.camera_states import State

router = APIRouter()


@router.websocket("/camera_feed")
async def websocket_endpoint(websocket: WebSocket):
    websoc_manager = websocket.app.websocket_manager
    camera = websocket.app.camera
    await websoc_manager.connect(websocket)

    try:
        camera_state = websocket.app.camera_state

        if camera_state != State.START_CAPTURE:
            raise WebSocketDisconnect(reason="Camera is not in Start Capture state")

        while camera_state != State.OFFLINE:
            camera_state = websocket.app.camera_state

            if camera_state == State.START_CAPTURE:
                await websocket.send_text(camera.get_image())
            
    except WebSocketDisconnect:
        websoc_manager.disconnect(websocket)
