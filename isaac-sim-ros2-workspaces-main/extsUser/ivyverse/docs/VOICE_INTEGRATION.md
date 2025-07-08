# Voice Integration for IvyVerse Extension

## Overview
The IvyVerse extension now includes OpenAI Realtime API integration for speech-to-speech functionality.

## Features
- **Voice Recording**: Click voice button to record speech
- **Audio Upload**: Upload audio files (.wav, .mp3, .m4a, .ogg, .flac)
- **Speech Responses**: Get audio responses from AI assistant
- **Transcription**: Speech appears in input field
- **Scene Context**: Voice responses include USD scene analysis

## Setup
1. Select "OpenAI GPT-4o" as LLM provider
2. Enter and save your OpenAI API key
3. Voice functionality automatically connects

## Components
- `audio_handler.py` - Audio recording/playback with PyAudio
- `realtime_api_client.py` - WebSocket communication with OpenAI
- `voice_interface.py` - Coordinator between UI and APIs
- `window.py` - UI integration with voice/upload buttons

## Usage
1. **Record**: Click voice button to start/stop recording
2. **Upload**: Click upload button to select audio file
3. **Transcribe**: Speech appears in input field automatically
4. **Send**: Click send for text and speech responses
5. **Listen**: Audio responses play automatically

## Requirements
```bash
pip install pyaudio>=0.2.11 websockets>=11.0 openai>=1.0.0
```

## Troubleshooting
- Check microphone permissions
- Verify OpenAI API key is saved
- Look for console logs for connection status
- Ensure audio devices are working