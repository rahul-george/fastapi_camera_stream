
"""
    Module: camera_states.py
    Author: Rahul George
    
    Description:
    
    License:
    
    Created on: 13-02-2024
    
"""
from enum import Enum


class State(int, Enum):
    OFFLINE = 1
    CONNECTED = 2
    START_CAPTURE = 3
    STOP_CAPTURE = 4
