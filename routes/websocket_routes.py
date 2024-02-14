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

        # if camera_state != State.START_CAPTURE:
        #     await websoc_manager.disconnect(websocket, reason="Camera is not in Start Capture state")
        #     raise WebSocketDisconnect(code=1001)

        capture_count = 0
        while camera_state != State.OFFLINE:
            camera_state = websocket.app.camera_state

            if camera_state == State.START_CAPTURE:
                await websocket.send_text(camera.get_image())

            capture_count += 1
            if capture_count % 100 == 0:
                print(f"{capture_count} Images captured")
            
    except WebSocketDisconnect:
        await websoc_manager.disconnect(websocket)
