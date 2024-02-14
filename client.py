"""
    Module: client.py
    Author: Rahul George

    Description:

    License:

    Created on: 14-02-2024

"""

from websockets.sync.client import connect


MAX_CAPTURE = 3
capture_count = 1
i = input("Select \n1. Connect,\n0.Exit\nMake Selection: ")
if i == "1":
    with connect("ws://localhost:8000/camera_feed", open_timeout=60, close_timeout=60) as websocket:
        while capture_count < MAX_CAPTURE:
            msg = websocket.recv()
            print(f">> Received: {msg}")
            capture_count += 1
