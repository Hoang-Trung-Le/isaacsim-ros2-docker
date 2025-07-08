"""
Audio Handler for IvyVerse Extension
Handles audio recording, playback, and file processing for OpenAI Realtime API integration.
"""

try:
    import pyaudio

    PYAUDIO_AVAILABLE = True
    AUDIO_BACKEND = "pyaudio"
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

    # Try sounddevice as fallback
    try:
        import sounddevice as sd
        import numpy as np

        SOUNDDEVICE_AVAILABLE = True
        AUDIO_BACKEND = "sounddevice"
    except ImportError:
        sd = None
        SOUNDDEVICE_AVAILABLE = False
        AUDIO_BACKEND = "none"

import wave
import threading
import queue
import time
import io
import base64
import carb
from typing import Callable, Optional


class AudioHandler:
    """
    Handles audio input and output using PyAudio for IvyVerse extension.
    """

    def __init__(self):
        self.audio_backend = AUDIO_BACKEND
        carb.log_info(f"Audio backend: {self.audio_backend}")

        if self.audio_backend == "none":
            carb.log_warn(
                "No audio libraries available. Audio functionality will be disabled."
            )
            self._init_no_audio()
            return
        elif self.audio_backend == "pyaudio":
            self._init_pyaudio()
        elif self.audio_backend == "sounddevice":
            self._init_sounddevice()

    def _init_no_audio(self):
        """Initialize with no audio support"""
        self.p = None
        self.input_stream = None
        self.output_stream = None
        self.audio_buffer = b""
        self.playback_queue = queue.Queue()

        # Audio configuration
        self.chunk_size = 1024
        self.channels = 1
        self.rate = 24000

        # Recording state
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None
        self.playback_thread = None

        # Callbacks
        self.on_audio_chunk = None
        self.on_recording_complete = None

    def _init_pyaudio(self):
        """Initialize with PyAudio"""
        self.p = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.audio_buffer = b""
        self.playback_queue = queue.Queue()

        # Audio configuration for OpenAI Realtime API
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 24000  # OpenAI Realtime API expects 24kHz

        # Recording state
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None
        self.playback_thread = None

        # Callbacks
        self.on_audio_chunk = None
        self.on_recording_complete = None

        # List available audio devices for debugging
        self._log_audio_devices()

    def _init_sounddevice(self):
        """Initialize with sounddevice"""
        self.p = None  # Not used for sounddevice
        self.input_stream = None
        self.output_stream = None
        self.audio_buffer = b""
        self.playback_queue = queue.Queue()

        # Audio configuration
        self.chunk_size = 1024
        self.channels = 1
        self.rate = 24000
        self.dtype = np.int16

        # Recording state
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None
        self.playback_thread = None

        # Callbacks
        self.on_audio_chunk = None
        self.on_recording_complete = None

        carb.log_info("Using sounddevice for audio")

    def _check_audio_availability(self) -> bool:
        """Check if any audio backend is available"""
        if self.audio_backend == "none":
            carb.log_error(
                "No audio libraries available. Please install PyAudio or sounddevice."
            )
            return False
        return True

    def _log_audio_devices(self):
        """Log available audio input devices for debugging"""
        if not self._check_audio_availability():
            return

        if self.audio_backend == "pyaudio" and self.p:
            carb.log_info("Available audio input devices (PyAudio):")
            for i in range(self.p.get_device_count()):
                device_info = self.p.get_device_info_by_index(i)
                if device_info["maxInputChannels"] > 0:
                    carb.log_info(f"Input Device ID {i} - {device_info['name']}")
        elif self.audio_backend == "sounddevice":
            carb.log_info("Available audio devices (sounddevice):")
            devices = sd.query_devices()
            carb.log_info(str(devices))

    def set_callbacks(
        self, on_audio_chunk: Callable = None, on_recording_complete: Callable = None
    ):
        """Set callback functions for audio events"""
        self.on_audio_chunk = on_audio_chunk
        self.on_recording_complete = on_recording_complete

    def start_recording(self, input_device_index: int = None) -> bool:
        """Start audio recording"""
        if self.is_recording:
            carb.log_warn("Recording already in progress")
            return False

        if self.audio_backend == "pyaudio":
            return self._start_recording_pyaudio(input_device_index)
        elif self.audio_backend == "sounddevice":
            return self._start_recording_sounddevice(input_device_index)

        return False

        # try:
        #     carb.log_info(f"Starting audio recording with device index: {input_device_index}")
        #     self.stream = self.p.open(
        #         format=self.format,
        #         channels=self.channels,
        #         rate=self.rate,
        #         input=True,
        #         frames_per_buffer=self.chunk_size,
        #         input_device_index=input_device_index,
        #     )

        #     self.is_recording = True
        #     self.audio_buffer = b""
        #     carb.log_info("Audio recording started")
        #     return True

        # except Exception as e:
        #     carb.log_error(f"Failed to start audio recording: {e}")
        #     self.is_recording = False
        #     return False

    def _start_recording_pyaudio(self, input_device_index: int = None) -> bool:
        """Start recording with PyAudio"""
        try:
            self.input_stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=input_device_index,
            )

            self.is_recording = True
            self.audio_buffer = b""

            # Start recording thread
            self.recording_thread = threading.Thread(
                target=self._recording_worker_pyaudio
            )
            self.recording_thread.daemon = True
            self.recording_thread.start()

            carb.log_info("Audio recording started (PyAudio)")
            return True

        except Exception as e:
            carb.log_error(f"Failed to start audio recording (PyAudio): {e}")
            self.is_recording = False
            return False

    def _start_recording_sounddevice(self, input_device_index: int = None) -> bool:
        """Start recording with sounddevice"""
        try:
            self.is_recording = True
            self.audio_buffer = b""

            # Start recording thread
            self.recording_thread = threading.Thread(
                target=self._recording_worker_sounddevice
            )
            self.recording_thread.daemon = True
            self.recording_thread.start()

            carb.log_info("Audio recording started (sounddevice)")
            return True

        except Exception as e:
            carb.log_error(f"Failed to start audio recording (sounddevice): {e}")
            self.is_recording = False
            return False

    def _recording_worker_pyaudio(self):
        """Worker thread for continuous audio recording with PyAudio"""
        while self.is_recording and self.input_stream:
            try:
                data = self.input_stream.read(
                    self.chunk_size, exception_on_overflow=False
                )
                self.audio_buffer += data

                # Send real-time audio chunk if callback is set
                if self.on_audio_chunk:
                    self.on_audio_chunk(data)

            except Exception as e:
                carb.log_error(f"Error in recording worker (PyAudio): {e}")
                break

    def _recording_worker_sounddevice(self):
        """Worker thread for continuous audio recording with sounddevice"""
        try:
            with sd.InputStream(
                samplerate=self.rate,
                channels=self.channels,
                dtype=self.dtype,
                blocksize=self.chunk_size,
            ) as stream:
                while self.is_recording:
                    data, overflowed = stream.read(self.chunk_size)
                    if overflowed:
                        carb.log_warn("Audio input overflow detected")

                    # Convert numpy array to bytes
                    audio_bytes = data.tobytes()
                    self.audio_buffer += audio_bytes

                    # Send real-time audio chunk if callback is set
                    if self.on_audio_chunk:
                        self.on_audio_chunk(audio_bytes)

        except Exception as e:
            carb.log_error(f"Error in recording worker (sounddevice): {e}")

    def stop_recording(self) -> bytes:
        """
        Stop audio recording and return recorded data

        Returns:
            bytes: Recorded audio data in WAV format
        """
        if not self._check_audio_availability():
            return b""

        if not self.is_recording:
            carb.log_warn("No recording in progress")
            return b""

        self.is_recording = False

        # Wait for recording thread to finish
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)

        # Close input stream (PyAudio only)
        if self.input_stream and self.audio_backend == "pyaudio":
            self.input_stream.stop_stream()
            self.input_stream.close()
            self.input_stream = None

        # Convert to WAV format
        wav_data = self._create_wav_data(self.audio_buffer)

        carb.log_info("Audio recording stopped")

        # Call completion callback
        if self.on_recording_complete:
            self.on_recording_complete(wav_data)

        return wav_data

    def _create_wav_data(self, audio_data: bytes) -> bytes:
        """
        Convert raw audio data to WAV format

        Args:
            audio_data: Raw audio bytes

        Returns:
            bytes: WAV formatted audio data
        """
        if not self._check_audio_availability():
            return b""

        if not audio_data:
            return b""

        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wav_file:
            wav_file.setnchannels(self.channels)

            if self.audio_backend == "pyaudio":
                wav_file.setsampwidth(self.p.get_sample_size(self.format))
            else:
                wav_file.setsampwidth(2)  # 16-bit audio

            wav_file.setframerate(self.rate)
            wav_file.writeframes(audio_data)
        return wav_io.getvalue()

    def record_chunk(self) -> Optional[bytes]:
        """Record a single chunk of audio (for real-time streaming)"""
        if self.stream and self.is_recording:
            try:
                data = self.stream.read(
                    self.chunk_size,
                    exception_on_overflow=False,
                )
                self.audio_buffer += data
                return data
            except Exception as e:
                carb.log_error(f"Error reading audio chunk: {e}")
                return None
        return None

    def play_audio(self, audio_data: bytes):
        """Play audio data (simple blocking version like test1.py)"""

        def play():
            try:
                stream = self.p.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    output=True,
                )
                stream.write(audio_data)
                stream.stop_stream()
                stream.close()
                carb.log_info("Audio playback completed")
            except Exception as e:
                carb.log_error(f"Error playing audio: {e}")

        # Use a separate thread for playback to avoid blocking
        playback_thread = threading.Thread(target=play)
        playback_thread.daemon = True
        playback_thread.start()

    def start_playback(self) -> bool:
        """Start audio playback system (for streaming playback)"""
        if self.is_playing:
            return True

        try:
            self.playback_stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                output=True,
                frames_per_buffer=self.chunk_size,
            )

            self.is_playing = True
            # Start playback thread
            self.playback_thread = threading.Thread(target=self._playback_worker)
            self.playback_thread.daemon = True
            self.playback_thread.start()

            carb.log_info("Audio playback started")
            return True

        except Exception as e:
            carb.log_error(f"Failed to start audio playback: {e}")
            return False

    def stop_playback(self):
        """Stop audio playback"""
        if not self.is_playing:
            return

        self.is_playing = False

        # Close output stream
        if hasattr(self, "playback_stream") and self.playback_stream:
            self.playback_stream.stop_stream()
            self.playback_stream.close()
            self.playback_stream = None

        carb.log_info("Audio playback stopped")

    def queue_audio_for_playback(self, audio_data: bytes):
        """Queue audio data for playback"""
        if not self.is_playing:
            self.start_playback()
        self.playback_queue.put(audio_data)

    def _playback_worker(self):
        """Worker thread for audio playback"""
        while self.is_playing:
            try:
                # Get audio data from queue with timeout
                audio_data = self.playback_queue.get(timeout=0.1)
                if (
                    audio_data
                    and hasattr(self, "playback_stream")
                    and self.playback_stream
                ):
                    self.playback_stream.write(audio_data)
            except queue.Empty:
                continue
            except Exception as e:
                carb.log_error(f"Error in playback worker: {e}")
                break

    def process_audio_file(self, file_path: str) -> Optional[bytes]:
        """Process an uploaded audio file and return raw audio data"""
        try:
            with open(file_path, "rb") as f:
                audio_data = f.read()
            carb.log_info(f"Processed audio file: {file_path}")
            return audio_data
        except Exception as e:
            carb.log_error(f"Failed to process audio file {file_path}: {e}")
            return None

    def cleanup(self):
        """Clean up audio resources"""
        # Stop recording
        if self.is_recording:
            self.stop_recording()

        # Stop playback
        if self.is_playing:
            self.stop_playback()

        # Terminate PyAudio
        if self.p:
            self.p.terminate()

        carb.log_info("Audio handler cleanup completed")
