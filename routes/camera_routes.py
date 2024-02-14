"""
    Module: camera_routes.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from utils.baslor_cam import Cam
from pypylon.genicam import RuntimeException
from utils.camera_states import State
from utils.dependencies import resolve_state


router = APIRouter()


@router.get("/devices")
async def enumerate_devices(request: Request):
    """Return all the enumerated devices. Expecting the Cam object is already initialized and added to request"""
    camera = request.app.camera
    devices = {f"{device.GetModelName()} - {device.GetSerialNumber()}": device for device in camera.enumerate_devices()}
    request.app.devices = devices
    return list(devices.keys())


@router.post("/connect_device")
async def connect_device(request: Request, device: str):
    """Expecting the serial number of a device and the endpoint will connect to that device"""
    next_state = await resolve_state(request, State.CONNECTED)
    # Todo: Potential bug because enumerate is not run before. Fix this with dependency injection.
    if device in request.app.devices:
        camera: Cam = request.app.camera        # TODO: We could store each device into a dictionary or something.
        try:
            camera.open_camera(request.app.devices[device])
        except RuntimeException as err:
            raise HTTPException(403, detail=str(err)) from err
        request.app.camera_state = State.CONNECTED
        return 'success'
    else:
        raise HTTPException(422, detail="Could not find the requested device!")


@router.post("/disconnect_device")
async def disconnect_device(request: Request, device: str):
    """Expect the serial number of the device to disconnect from"""
    next_state = await resolve_state(request, State.OFFLINE)
    if device in request.app.devices:
        camera: Cam = request.app.camera
        camera.close_camera()
        request.app.camera_state = State.OFFLINE
        return 'success'
    else:
        raise HTTPException(422, detail="Could not find the requested device!")


@router.post("/start_capture")
async def start_capture(request: Request):
    """Expect the serial number of the device to disconnect from"""
    next_state = await resolve_state(request, State.START_CAPTURE)
    camera: Cam = request.app.camera
    camera.start_capture(None)
    request.app.camera_state = next_state
    return next_state.name


@router.post("/stop_capture")
async def stop_capture(request: Request):
    """Expect the serial number of the device to disconnect from"""
    next_state = await resolve_state(request, State.STOP_CAPTURE)
    camera: Cam = request.app.camera
    camera.stop_capture()
    request.app.camera_state = next_state
    return next_state.name

