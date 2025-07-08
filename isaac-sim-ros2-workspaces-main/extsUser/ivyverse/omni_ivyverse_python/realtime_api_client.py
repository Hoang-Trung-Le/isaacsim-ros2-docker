"""
OpenAI Realtime API Client for IvyVerse Extension
Handles WebSocket communication with OpenAI Realtime API for speech-to-speech functionality.
"""

import asyncio
import websockets
import json
import base64
import ssl
import carb
from typing import Callable, Optional, Dict, Any


class RealtimeAPIClient:
    """
    Client for interacting with the OpenAI Realtime API via WebSocket for IvyVerse.
    """

    def __init__(self, api_key: str, voice: str = "alloy"):
        self.api_key = api_key
        self.voice = voice
        self.websocket = None
        self.is_connected = False
        self.audio_buffer = b""

        # WebSocket Configuration
        self.url = "wss://api.openai.com/v1/realtime"
        self.model = "gpt-4o-mini-realtime-preview-2024-12-17"

        # SSL Configuration
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # Callbacks
        self.on_audio_delta = None
        self.on_audio_done = None
        self.on_transcript_delta = None
        self.on_error = None

        # Session configuration
        self.session_config = {
            "modalities": ["audio", "text"],
            "instructions": self._get_instructions(),
            "voice": self.voice,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "turn_detection": None,  # Manual turn detection
            "input_audio_transcription": {"model": "whisper-1"},
            "temperature": 0.7,
        }

    def _get_instructions(self) -> str:
        """Get system instructions for the AI assistant"""
        return """You are an industrial USD scene assistant for NVIDIA Omniverse integrated with IvyVerse.
You help users understand and analyze their 3D scenes through voice interaction.
Be concise, clear, and helpful in your audio responses.
Focus on scene analysis, USD properties, materials, lighting, and workflow optimization.
Keep responses conversational and under 30 seconds when possible."""

    def set_callbacks(
        self,
        on_audio_delta: Callable[[bytes], None] = None,
        on_audio_done: Callable[[], None] = None,
        on_text_delta: Callable[[str], None] = None,
        on_transcript_delta: Callable[[str], None] = None,
        on_error: Callable[[str], None] = None,
        on_speech_started: Callable[[], None] = None,
        on_speech_stopped: Callable[[], None] = None,
    ):
        """Set callback functions for various events"""
        self.on_audio_delta = on_audio_delta
        self.on_audio_done = on_audio_done
        self.on_transcript_delta = on_transcript_delta
        self.on_error = on_error

    async def connect(self) -> bool:
        """Connect to the OpenAI Realtime API WebSocket"""
        try:
            carb.log_info("Connecting to OpenAI Realtime API...")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "OpenAI-Beta": "realtime=v1",
            }

            # Connect to WebSocket
            self.websocket = await websockets.connect(
                f"{self.url}?model={self.model}",
                extra_headers=headers,
                ssl=self.ssl_context,
            )

            self.is_connected = True
            carb.log_info("Successfully connected to OpenAI Realtime API")

            # Configure session
            await self._send_event(
                {"type": "session.update", "session": self.session_config}
            )

            carb.log_info("Session configured successfully")
            return True

        except Exception as e:
            error_msg = f"Failed to connect to Realtime API: {str(e)}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)
            return False

    async def disconnect(self):
        """Disconnect from the WebSocket"""
        if self.websocket and self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            carb.log_info("Disconnected from OpenAI Realtime API")

    async def _send_event(self, event: Dict[str, Any]):
        """Send an event to the WebSocket server"""
        if not self.websocket or not self.is_connected:
            carb.log_error("WebSocket not connected")
            return

        try:
            await self.websocket.send(json.dumps(event))
            carb.log_info(f"Event sent - type: {event['type']}")
        except Exception as e:
            carb.log_error(f"Failed to send event: {e}")

    async def send_text_message(self, text: str):
        """Send a text message to the conversation"""
        carb.log_info(f"Sending text message: {text[:50]}...")
        event = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        }
        await self._send_event(event)
        await self._send_event({"type": "response.create"})

    async def process_audio_input(self, audio_data: bytes):
        """Process audio input"""
        try:
            # Send audio data in chunks
            chunk_size = 1024
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i : i + chunk_size]
                base64_chunk = base64.b64encode(chunk).decode("utf-8")
                await self._send_event(
                    {"type": "input_audio_buffer.append", "audio": base64_chunk}
                )
                # Small delay to prevent overwhelming the API
                await asyncio.sleep(0.01)

            # Commit buffer and request response (same as test1.py)
            await self._send_event({"type": "input_audio_buffer.commit"})
            await self._send_event({"type": "response.create"})
            carb.log_info("Audio input processed and response requested")

        except Exception as e:
            error_msg = f"Failed to process audio input: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    async def listen_for_events(self):
        """Listen for incoming events from WebSocket"""
        try:
            while self.is_connected and self.websocket:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    event = json.loads(message)
                    await self._handle_event(event)
                except asyncio.TimeoutError:
                    continue
                except websockets.ConnectionClosed:
                    carb.log_warn("WebSocket connection closed")
                    self.is_connected = False
                    break
        except Exception as e:
            error_msg = f"Error listening for events: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    async def _handle_event(self, event: Dict[str, Any]):
        """Handle incoming events"""
        event_type = event.get("type")
        carb.log_info(f"Received event type: {event_type}")

        try:
            if event_type == "error":
                error_msg = event.get("error", {}).get("message", "Unknown error")
                carb.log_error(f"API Error: {error_msg}")
                if self.on_error:
                    self.on_error(error_msg)

            elif event_type == "conversation.item.input_audio_transcription.completed":
                # Audio transcription completed
                transcript = event.get("transcript", "")
                if self.on_transcript_delta and transcript:
                    self.on_transcript_delta(transcript)
                    carb.log_info(f"Transcription: {transcript}")

            elif event_type == "response.audio.delta":
                # Audio response chunk
                audio_delta = event.get("delta", "")
                if audio_delta and self.on_audio_delta:
                    audio_data = base64.b64decode(audio_delta)
                    self.audio_buffer += audio_data
                    self.on_audio_delta(audio_data)

            elif event_type == "response.audio.done":
                # Audio response completed
                carb.log_info("Audio response completed")
                if self.on_audio_done:
                    self.on_audio_done()
                self.audio_buffer = b""

            elif event_type == "response.done":
                carb.log_info("Response generation completed")

            elif event_type == "conversation.item.created":
                carb.log_info("Conversation item created")

            else:
                carb.log_info(f"Unhandled event type: {event_type}")

        except Exception as e:
            carb.log_error(f"Error handling event {event_type}: {e}")

    def update_scene_context(self, scene_context: str):
        """Update the session with new scene context"""
        enhanced_instructions = (
            self._get_instructions() + f"\n\nCurrent Scene Context:\n{scene_context}"
        )
        self.session_config["instructions"] = enhanced_instructions

        # Send updated session config if connected
        if self.is_connected:
            asyncio.ensure_future(
                self._send_event(
                    {"type": "session.update", "session": self.session_config}
                )
            )

    def set_voice(self, voice: str):
        """Update the voice setting"""
        self.voice = voice
        self.session_config["voice"] = voice

        # Send updated session config if connected
        if self.is_connected:
            asyncio.ensure_future(
                self._send_event(
                    {"type": "session.update", "session": self.session_config}
                )
            )
