#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import base64
import json
import asyncio
import websockets
import threading
import argparse
from datetime import datetime


class ImageStreamer(Node):
    def __init__(self, topic_name="/camera/raw_image", websocket_port=8765):
        super().__init__("image_streamer")

        # Parameters
        self.topic_name = topic_name
        self.websocket_port = websocket_port
        self.bridge = CvBridge()
        self.latest_frame = None
        self.connected_clients = set()

        # Create subscriber to the ROS2 image topic
        self.subscription = self.create_subscription(
            Image, self.topic_name, self.image_callback, 10
        )

        self.get_logger().info(
            f"Subscribed to {self.topic_name}, streaming on websocket port {self.websocket_port}"
        )

        # Start WebSocket server in a separate thread
        self.websocket_thread = threading.Thread(target=self.start_websocket_server)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def image_callback(self, msg):
        """Process incoming image messages from ROS2"""
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # Store latest frame
            self.latest_frame = cv_image

            # Log message rate (once every ~5 seconds)
            timestamp = datetime.now()
            if (
                hasattr(self, "last_log_time")
                and (timestamp - self.last_log_time).total_seconds() < 5
            ):
                pass
            else:
                self.get_logger().info(
                    f"Received image on {self.topic_name} ({len(self.connected_clients)} clients connected)"
                )
                self.last_log_time = timestamp

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def start_websocket_server(self):
        """Start the WebSocket server in the background"""
        asyncio.run(self.run_websocket_server())

    async def run_websocket_server(self):
        """Run the WebSocket server"""

        async def handler(websocket, path):
            # Register new client
            self.connected_clients.add(websocket)
            try:
                self.get_logger().info(f"Client connected: {websocket.remote_address}")

                # Keep connection alive and wait for client messages
                async for message in websocket:
                    # Client can send commands if needed
                    pass

            except websockets.exceptions.ConnectionClosed:
                pass
            finally:
                # Remove client on disconnection
                self.connected_clients.remove(websocket)
                self.get_logger().info(
                    f"Client disconnected: {websocket.remote_address}"
                )

        # Start WebSocket server
        server = await websockets.serve(handler, "0.0.0.0", self.websocket_port)

        # Start background task to send frames to all clients
        asyncio.create_task(self.broadcast_frames())

        # Keep server running
        await server.wait_closed()

    async def broadcast_frames(self):
        """Send frames to all connected clients"""
        while True:
            if self.latest_frame is not None and self.connected_clients:
                # Encode image to JPEG
                try:
                    _, jpeg_image = cv2.imencode(
                        ".jpg", self.latest_frame, [cv2.IMWRITE_JPEG_QUALITY, 80]
                    )

                    # Convert to base64 for sending over WebSocket
                    encoded_image = base64.b64encode(jpeg_image).decode("utf-8")

                    # Create message with frame data
                    message = json.dumps(
                        {
                            "topic": self.topic_name,
                            "image": encoded_image,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    # Send to all connected clients
                    websockets_to_remove = set()
                    for websocket in self.connected_clients:
                        try:
                            await websocket.send(message)
                        except websockets.exceptions.ConnectionClosed:
                            websockets_to_remove.add(websocket)

                    # Clean up any closed connections
                    for websocket in websockets_to_remove:
                        self.connected_clients.remove(websocket)

                except Exception as e:
                    self.get_logger().error(f"Error encoding/sending frame: {e}")

            # Control streaming rate
            await asyncio.sleep(0.033)  # ~30 fps


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Stream ROS2 image topics via WebSocket"
    )
    parser.add_argument(
        "--topic", type=str, default="/raw_image", help="ROS2 image topic to stream"
    )
    parser.add_argument("--port", type=int, default=8765, help="WebSocket server port")

    args = parser.parse_args()

    rclpy.init()
    streamer = ImageStreamer(topic_name=args.topic, websocket_port=args.port)

    try:
        rclpy.spin(streamer)
    except KeyboardInterrupt:
        pass
    finally:
        streamer.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
