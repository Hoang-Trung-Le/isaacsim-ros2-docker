import websocket
import json
import base64
import cv2
import numpy as np


def on_message(ws, message):
    data = json.loads(message)
    if data["topic"] == "/raw_image":
        img_data = base64.b64decode(data["msg"]["data"])
        np_img = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        # Process with Metropolis (e.g., inference)
        print("Received image for Metropolis processing")


ws = websocket.WebSocketApp("ws://192.168.1.100:9090", on_message=on_message)
ws.run_forever()
