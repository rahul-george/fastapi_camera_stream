"""
    Module: camera_routes.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from utils.baslor_cam import Cam
from utils.camera_states import State
from utils.dependencies import resolve_state


router = APIRouter()


@router.get("/devices")
def enumerate_devices(request: Request):
    """Return all the enumerated devices. Expecting the Cam object is already initialized and added to request"""
    camera = request.app.camera
    devices = {f"{device.GetModelName()} - {device.GetSerialNumber()}": device for device in camera.enumerate_devices()}
    request.app.devices = devices
    return devices


@router.post("/connect_device")
def connect_device(request: Request, device: str):
    """Expecting the serial number of a device and the endpoint will connect to that device"""
    next_state = resolve_state(State.CONNECTED)
    if device in request.app.devices:
        camera: Cam = request.app.camera        # TODO: We could store each device into a dictionary or something. 
        camera.open_camera(request.app.device[device])

        request.app.camera_state = State.CONNECTED
    else:
        raise HTTPException("Could not find the requested device!")


@router.post("/disconnect_device")
def disconnect_device(request: Request, device: str):
    """Expect the serial number of the device to disconnect from"""
    next_state = resolve_state(State.OFFLINE)
    if device in request.app.devices:
        camera: Cam = request.app.camera
        camera.close_camera()
        request.app.camera_state = State.OFFLINE
    else:
        raise HTTPException("Could not find the requested device!")


@router.post("/start_capture")
def start_capture(request: Request):
    """Expect the serial number of the device to disconnect from"""
    camera: Cam = request.app.camera
    camera.start_capture()
    next_state = resolve_state(State.START_CAPTURE)


@router.post("/stop_capture")
def stop_capture(request: Request):
    """Expect the serial number of the device to disconnect from"""
    camera: Cam = request.app.camera
    camera.start_capture()
    next_state = resolve_state(State.STOP_CAPTURE)
