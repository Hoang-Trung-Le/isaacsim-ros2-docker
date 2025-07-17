"""
Voice Interface for IvyVerse Extension
Coordinates audio recording, transcription, and speech responses between UI and APIs.
"""

import asyncio
import carb
import os
import re
from typing import Optional, Callable
from .audio_handler import AudioHandler
from .realtime_api_client import RealtimeAPIClient
from .rag_manager import RAGManager


class VoiceInterface:
    """
    Manages voice interaction workflow for IvyVerse extension.
    Coordinates between UI, audio handling, and OpenAI Realtime API.
    """

    def __init__(self):
        self.audio_handler = AudioHandler()
        self.api_client = None
        self.rag_manager = RAGManager()
        self.use_rag = True  # Enable RAG for voice interactions
        self.is_recording = False
        self.is_connected = False
        self.current_transcript = ""
        self.current_text_response = ""

        # Callbacks for UI updates
        self.on_transcript_update = None
        self.on_status_update = None
        self.on_error = None
        self.on_audio_playback_start = None
        self.on_audio_playback_end = None
        self.on_text_response_delta = None
        self.on_text_response_done = None
        self.conversation_mode = False
        self.conversation_streaming = False
        self.on_speech_started = None
        self.on_speech_stopped = None

    def _detect_language(self, text: str) -> str:
        """Detect if the text contains Japanese characters"""
        # Check for Japanese characters (Hiragana, Katakana, Kanji)
        japanese_pattern = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]")
        if japanese_pattern.search(text):
            return "Japanese"
        return "English"

    async def _get_rag_context(self, user_query: str) -> Optional[str]:
        """Get RAG context for the user query"""
        if not self.use_rag:
            return None

        try:
            # Notify UI that RAG is being used
            if self.on_status_update:
                self.on_status_update("Retrieving context from knowledge base...", True)

            # Initialize RAG if not already done
            if not self.rag_manager.rag_initialized:
                success = self.rag_manager.initialize_rag()
                if not success:
                    carb.log_warn("RAG initialization failed for voice interface")
                    if self.on_status_update:
                        self.on_status_update("RAG initialization failed", False)
                    return None

            # Detect language for better RAG responses
            detected_language = self._detect_language(user_query)
            carb.log_info(
                f"Voice RAG query - Language: {detected_language}, Query: {user_query[:50]}..."
            )

            # Query RAG
            rag_response = await self.rag_manager.query_rag(
                user_query, detected_language
            )

            if rag_response and not rag_response.startswith("Error:"):
                carb.log_info(
                    f"RAG context retrieved for voice: {len(rag_response)} characters"
                )
                if self.on_status_update:
                    self.on_status_update(
                        "Context retrieved from knowledge base", False
                    )
                return rag_response
            else:
                carb.log_warn(
                    f"RAG returned empty or error response: {rag_response[:100] if rag_response else 'None'}"
                )
                if self.on_status_update:
                    self.on_status_update(
                        "No relevant context found in knowledge base", False
                    )
                return None

        except Exception as e:
            carb.log_error(f"Error getting RAG context for voice: {str(e)}")
            if self.on_status_update:
                self.on_status_update(f"RAG error: {str(e)}", False)
            return None

    def set_ui_callbacks(
        self,
        on_transcript_update: Callable[[str], None] = None,
        on_status_update: Callable[[str, bool], None] = None,
        on_error: Callable[[str], None] = None,
        on_audio_playback_start: Callable[[], None] = None,
        on_audio_playback_end: Callable[[], None] = None,
        on_text_response_delta: Callable[[str], None] = None,
        on_text_response_done: Callable[[], None] = None,
        on_speech_started: Callable[[], None] = None,
        on_speech_stopped: Callable[[], None] = None,
    ):
        """Set UI callback functions"""
        self.on_transcript_update = on_transcript_update
        self.on_status_update = on_status_update
        self.on_error = on_error
        self.on_audio_playback_start = on_audio_playback_start
        self.on_audio_playback_end = on_audio_playback_end
        self.on_text_response_delta = on_text_response_delta
        self.on_text_response_done = on_text_response_done
        self.on_speech_started = on_speech_started
        self.on_speech_stopped = on_speech_stopped

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
                on_text_delta=self._on_text_response_delta,
                on_text_done=self._on_text_response_done,
                on_speech_started=self._on_speech_started,
                on_speech_stopped=self._on_speech_stopped,
                on_rag_context_needed=self._on_rag_context_needed,
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

    async def enable_conversation_mode(self):
        """Enable conversation mode with server VAD and RAG support"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return False

        try:
            await self.api_client.enable_conversation_mode()
            self.conversation_mode = True

            # Set up real-time audio streaming callback
            self.audio_handler.set_realtime_callback(self._stream_audio_chunk)

            carb.log_info("Conversation mode enabled with RAG support")
            return True
        except Exception as e:
            error_msg = f"Failed to enable conversation mode: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)
            return False

    async def disable_conversation_mode(self):
        """Disable conversation mode"""
        if not self.conversation_mode:
            return

        try:
            await self.api_client.disable_conversation_mode()
            self.conversation_mode = False

            # Stop streaming if active
            if self.conversation_streaming:
                await self.stop_conversation()

            # Remove real-time callback
            self.audio_handler.set_realtime_callback(None)

            carb.log_info("Conversation mode disabled")
        except Exception as e:
            error_msg = f"Failed to disable conversation mode: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    async def start_conversation(self):
        """Start conversation streaming"""
        if not self.conversation_mode or not self.is_connected:
            self._handle_error("Conversation mode not enabled or not connected")
            return False

        try:
            # Start audio recording with streaming
            success = self.audio_handler.start_recording()
            if not success:
                return False

            # Enable streaming in API client
            await self.api_client.start_conversation_streaming()
            self.conversation_streaming = True

            carb.log_info("Conversation started")
            return True
        except Exception as e:
            error_msg = f"Failed to start conversation: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)
            return False

    async def stop_conversation(self):
        """Stop conversation streaming"""
        if not self.conversation_streaming:
            return

        try:
            # Stop audio recording
            self.audio_handler.stop_recording()

            # Stop streaming in API client
            await self.api_client.stop_conversation_streaming()
            self.conversation_streaming = False

            carb.log_info("Conversation stopped")
        except Exception as e:
            error_msg = f"Failed to stop conversation: {e}"
            carb.log_error(error_msg)
            if self.on_error:
                self.on_error(error_msg)

    def _stream_audio_chunk(self, audio_chunk: bytes):
        """Handle real-time audio chunks for conversation mode"""
        if self.conversation_streaming and self.api_client:
            asyncio.ensure_future(self.api_client.stream_audio_chunk(audio_chunk))

    # NEW CALLBACK METHODS FOR CONVERSATION MODE:
    def _on_speech_started(self):
        """Handle speech detection started"""
        carb.log_info("Speech started")
        if self.on_speech_started:
            self.on_speech_started()

    def _on_speech_stopped(self):
        """Handle speech detection stopped"""
        carb.log_info("Speech stopped - response will be generated")
        if self.on_speech_stopped:
            self.on_speech_stopped()

    def _on_rag_context_needed(self, transcript: str):
        """Handle RAG context needed for conversation mode"""
        if self.conversation_mode:
            # Asynchronously get RAG context and update session
            asyncio.ensure_future(self._update_conversation_with_rag(transcript))

    async def _update_conversation_with_rag(self, transcript: str):
        """Update conversation session with RAG context"""
        try:
            rag_context = await self._get_rag_context(transcript)

            if rag_context:
                # Update session with RAG context for this conversation turn
                enhanced_instructions = (
                    self.api_client._get_instructions()
                    + f"\n\nRelevant context from knowledge base for current query:\n{rag_context}"
                )
                await self.api_client.update_session_instructions(enhanced_instructions)
                carb.log_info("Conversation session updated with RAG context")

        except Exception as e:
            carb.log_error(f"Error updating conversation with RAG: {e}")

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

    async def request_voice_response(self):
        """Request a voice response from the API"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return
        try:
            if self.api_client:
                await self.api_client.request_voice_response()
                carb.log_info("Voice response requested")
        except Exception as e:
            error_msg = f"Error requesting voice response: {e}"
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

    async def send_dictation_response(self, text: str):
        """Send text message with RAG context and get speech response"""
        if not self.is_connected:
            self._handle_error("Voice interface not connected")
            return

        try:
            if self.api_client:
                # Get RAG context before sending to OpenAI
                rag_context = await self._get_rag_context(text)

                if rag_context:
                    # Update session with RAG context
                    enhanced_instructions = (
                        self.api_client._get_instructions()
                        + f"\n\nRelevant context from knowledge base:\n{rag_context}"
                    )
                    await self.api_client.update_session_instructions(
                        enhanced_instructions
                    )
                    carb.log_info("Session updated with RAG context for voice response")

                # Send the original user text (not modified by RAG)
                await self.api_client.send_text_message(text)
                carb.log_info(
                    f"Sent text with RAG context for speech response: {text[:50]}..."
                )

        except Exception as e:
            error_msg = f"Error sending text message with RAG: {e}"
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

    def enable_rag(self, enable: bool):
        """Enable or disable RAG for voice interactions"""
        self.use_rag = enable
        carb.log_info(
            f"RAG for voice interactions: {'enabled' if enable else 'disabled'}"
        )

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

    def _on_text_response_delta(self, text_delta: str):
        """Handle text response updates"""
        self.current_text_response += text_delta
        if self.on_text_response_delta:
            self.on_text_response_delta(text_delta)

    def _on_text_response_done(self, text_done: str):
        """Handle completion of text response"""
        carb.log_info(f"Text response completed: {text_done}")
        if self.on_text_response_done:
            self.on_text_response_done(text_done)
        self.current_text_response = ""

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
