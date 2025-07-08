"""
Voice Interface for IvyVerse Extension
Coordinates audio recording, transcription, and speech responses between UI and APIs.
"""

import asyncio
import carb
import os
from typing import Optional, Callable
from .audio_handler import AudioHandler
from .realtime_api_client import RealtimeAPIClient


class VoiceInterface:
    """
    Manages voice interaction workflow for IvyVerse extension.
    Coordinates between UI, audio handling, and OpenAI Realtime API.
    """

    def __init__(self):
        self.audio_handler = AudioHandler()
        self.api_client = None
        self.is_recording = False
        self.is_connected = False
        self.current_transcript = ""

        # Callbacks for UI updates
        self.on_transcript_update = None
        self.on_status_update = None
        self.on_error = None
        self.on_audio_playback_start = None
        self.on_audio_playback_end = None

    def set_ui_callbacks(
        self,
        on_transcript_update: Callable[[str], None] = None,
        on_status_update: Callable[[str, bool], None] = None,
        on_error: Callable[[str], None] = None,
        on_audio_playback_start: Callable[[], None] = None,
        on_audio_playback_end: Callable[[], None] = None,
    ):
        """Set UI callback functions"""
        self.on_transcript_update = on_transcript_update
        self.on_status_update = on_status_update
        self.on_error = on_error
        self.on_audio_playback_start = on_audio_playback_start
        self.on_audio_playback_end = on_audio_playback_end

    async def initialize_connection(self, api_key: str, voice: str = "alloy") -> bool:
        """Initialize connection to OpenAI Realtime API"""
        if self.is_connected:
            await self.disconnect()

        try:
            self.api_client = RealtimeAPIClient(api_key, voice)

            # Set up API client callbacks
            self.api_client.set_callbacks(
                on_audio_delta=self._on_audio_delta,
                on_audio_done=self._on_audio_done,
                on_transcript_delta=self._on_transcript_delta,
                on_error=self._on_api_error,
            )

            # Connect to API
            success = await self.api_client.connect()
            if success:
                self.is_connected = True
                # Start listening for events
                asyncio.ensure_future(self.api_client.listen_for_events())
                carb.log_info("Voice interface connected successfully")
                return True
            else:
                carb.log_error("Failed to connect voice interface")
                return False

        except Exception as e:
            error_msg = f"Failed to initialize voice connection: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)
            return False

    async def disconnect(self):
        """Disconnect from OpenAI Realtime API"""
        if self.api_client:
            await self.api_client.disconnect()
            self.api_client = None
        self.is_connected = False
        carb.log_info("Voice interface disconnected")

    def start_recording(self):
        """Start voice recording"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return

        if self.is_recording:
            carb.log_warn("Recording already in progress")
            return

        success = self.audio_handler.start_recording()
        if success:
            self.is_recording = True
            self.current_transcript = ""
            carb.log_info("Voice recording started")
        else:
            self._handle_error("Failed to start recording")

    def stop_recording(self):
        """Stop voice recording and process audio"""
        if not self.is_recording:
            return

        self.is_recording = False
        audio_data = self.audio_handler.stop_recording()

        if audio_data and self.api_client:
            # Process the recorded audio
            asyncio.ensure_future(self._process_recorded_audio(audio_data))

        carb.log_info("Voice recording stopped")

    async def _process_recorded_audio(self, audio_data: bytes):
        """Process recorded audio data"""
        try:
            if self.api_client:
                await self.api_client.process_audio_input(audio_data)
        except Exception as e:
            error_msg = f"Error processing recorded audio: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    async def process_uploaded_audio(self, file_path: str):
        """Process an uploaded audio file"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return

        try:
            # Read audio file
            audio_data = self.audio_handler.process_audio_file(file_path)
            if audio_data and self.api_client:
                await self.api_client.process_audio_input(audio_data)
                carb.log_info(f"Processed uploaded audio: {file_path}")
            else:
                self._handle_error("Failed to process audio file")

        except Exception as e:
            error_msg = f"Error processing uploaded audio: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    async def send_text_with_speech_response(self, text: str):
        """Send text message and get speech response"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return

        try:
            if self.api_client:
                await self.api_client.send_text_message(text)
                carb.log_info(f"Sent text for speech response: {text[:50]}...")
        except Exception as e:
            error_msg = f"Error sending text message: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    def update_scene_context(self, scene_context: str):
        """Update scene context for the API"""
        if self.api_client:
            self.api_client.update_scene_context(scene_context)

    def set_voice(self, voice: str):
        """Update voice setting"""
        if self.api_client:
            self.api_client.set_voice(voice)

    # API event callbacks
    def _on_audio_delta(self, audio_data: bytes):
        """Handle incoming audio response chunks"""
        # Start playback if not already started
        if not self.audio_handler.is_playing:
            self.audio_handler.start_playback()
            if self.on_audio_playback_start:
                self.on_audio_playback_start()

        # Queue audio for playback
        self.audio_handler.queue_audio_for_playback(audio_data)

    def _on_audio_done(self):
        """Handle completion of audio response"""
        carb.log_info("Audio response completed")
        if self.on_audio_playback_end:
            self.on_audio_playback_end()

    def _on_transcript_delta(self, transcript: str):
        """Handle transcription updates"""
        self.current_transcript = transcript
        if self.on_transcript_update:
            self.on_transcript_update(transcript)
        carb.log_info(f"Transcript: {transcript}")

    def _on_api_error(self, error_message: str):
        """Handle API errors"""
        self._handle_error(f"API Error: {error_message}")

    def _handle_error(self, error_message: str):
        """Handle errors and notify UI"""
        carb.log_error(error_message)
        if self.on_error:
            self.on_error(error_message)

    def cleanup(self):
        """Clean up resources"""
        if self.is_recording:
            self.stop_recording()

        # Cleanup audio handler
        self.audio_handler.cleanup()

        # Disconnect from API
        if self.is_connected:
            asyncio.ensure_future(self.disconnect())

        carb.log_info("Voice interface cleanup completed")
