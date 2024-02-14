"""
    Module: dependencies.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
from fastapi import Request, HTTPException

from utils.camera_states import State


async def resolve_state(request: Request, state: State):
    current_state = request.app.camera_state
    if current_state == State.OFFLINE and state == State.CONNECTED:
        print("Ready for use")
        return State.CONNECTED
    elif current_state == State.CONNECTED and state == State.OFFLINE:
        print("Ready for shut down")
        return State.OFFLINE
    elif current_state == State.CONNECTED and state == State.START_CAPTURE:
        print("prepare for testing")
        return State.START_CAPTURE
    elif current_state == State.START_CAPTURE and state == State.STOP_CAPTURE:
        print("prepare to pause")
        return State.STOP_CAPTURE
    elif current_state == State.STOP_CAPTURE and state == State.START_CAPTURE:
        print("prepare to stop")
        return State.START_CAPTURE
    elif current_state == State.STOP_CAPTURE and state == State.OFFLINE:
        print("prepare to stop")
        return State.OFFLINE
    elif current_state == State.START_CAPTURE and state == State.OFFLINE:
        print("prepare to stop")
        return State.OFFLINE
    else:
        raise HTTPException(403, "Not an allowed state transition")
