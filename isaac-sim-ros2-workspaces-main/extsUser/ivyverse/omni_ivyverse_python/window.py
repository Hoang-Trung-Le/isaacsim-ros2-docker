import omni.ui as ui
import carb
import asyncio
import datetime
import os
from .llm_manager import LLMManager
from .scene_analyzer import SceneAnalyzer
from .chat_interface import ChatInterface
from .voice_interface import VoiceInterface

# from isaacsim.gui.components.menu import make_menu_item_description
# from isaacsim.gui.components.style import VERTICAL_SPACING
# from isaacsim.gui.components.ui_utils import *
from omni.kit.menu.utils import MenuItemDescription, add_menu_items, remove_menu_items

# from omni.ui import color as cl
from omni.kit.window.filepicker.dialog import FilePickerDialog
import omni.ui.color_utils as cl
from .style import ivyverse_style


class IvyverseWindow(ui.Window):
    """Main window for Ivyverse extension"""

    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
        self.frame.style = ivyverse_style
        self.frame.set_build_fn(self._build_window)
        self.llm_manager = LLMManager()
        self.scene_analyzer = SceneAnalyzer()
        self.chat_interface = None
        self.voice_interface = VoiceInterface()
        self.providers = ["NVIDIA NIM", "OpenAI GPT-4o"]
        self.default_provider = 1
        # self._style_sheet = StyleSheet() if STYLESHEET_LOADED else None

        # Voice interface state
        self._voice_connected = False
        self._voice_recording = False
        self._voice_response_mode = False  # Boolean flag for voice response
        self._input_filepicker = None

        # Initialize voice interface callbacks
        self._setup_voice_callbacks()

    def _build_window(self):
        with self.frame:
            with ui.VStack(
                height=0,
                # style={"debug_color": cl.color.red}
            ):
                # Header

                with ui.Frame(width=200, height=50):
                    ui.Image(name="ivyverse-logo")
                with ui.HStack(
                    height=30,
                    style={
                        "padding": 0,
                        "margin": 5,
                    },
                ):
                    with ui.VStack():
                        ui.Label(
                            "IvyVerse",
                            name="header-main",
                        )
                        ui.Label(
                            "USD Scene Copilot",
                            name="header-sub",
                        )
                    ui.Spacer()

                # Main content area
                with ui.HStack(style={"padding": 0}, height=ui.Fraction(1)):
                    # Left sidebar for configuration
                    with ui.VStack(
                        width=300,
                        style={
                            "padding": 10,
                        },
                    ):
                        # Configuration Section
                        with ui.CollapsableFrame(
                            "Configuration", height=0, style={"margin": 5}
                        ):
                            with ui.VStack(spacing=8, style={"padding": 8}):
                                # LLM Selection
                                ui.Label("LLM Provider:")
                                self._llm_combo = ui.ComboBox(
                                    self.default_provider,  # Select the second item (OpenAI GPT-4o) by default
                                    *self.providers,
                                )

                                # Connect the callback to handle selection changes
                                self._llm_combo.model.add_item_changed_fn(
                                    self._on_llm_changed
                                )

                                # API Key
                                ui.Label("API Key:")
                                with ui.HStack(height=30):
                                    self._api_key_field = ui.StringField(
                                        password_mode=True,
                                        style={"background_color": cl.color.black},
                                    )
                                    self._save_button = ui.Button(
                                        "Save",
                                        width=60,
                                        clicked_fn=self._save_api_key,
                                    )

                        # Scene Information
                        with ui.CollapsableFrame(
                            "Scene Information",
                            collapsed=False,
                            height=0,
                            style={"margin": 5},
                        ):
                            with ui.VStack(spacing=8, style={"padding": 8}):
                                self._scene_info_label = ui.Label(
                                    "No scene loaded",
                                    word_wrap=True,
                                )
                                ui.Button(
                                    "Analyze Current Scene",
                                    height=30,
                                    clicked_fn=self._analyze_scene,
                                )

                        # Export Options
                        with ui.CollapsableFrame(
                            "Export Options", height=0, style={"margin": 5}
                        ):
                            with ui.VStack(spacing=8, style={"padding": 8}):
                                ui.Button(
                                    "Export Chat History",
                                    clicked_fn=self._export_chat,
                                    # style=get_style(self._style_sheet, "button"),
                                )
                                ui.Button(
                                    "Export Scene Analysis",
                                    clicked_fn=self._export_analysis,
                                    # style=get_style(self._style_sheet, "button"),
                                )

                    # Right panel for chat interface
                    with ui.VStack():
                        # Chat header
                        with ui.HStack(
                            height=40,
                        ):
                            ui.Label(
                                "Assistant Chat",
                                name="header-chat",
                            )
                            ui.Spacer()

                        # Chat history
                        self._chat_history = ui.ScrollingFrame(
                            height=ui.Fraction(1),
                            name="chat-history",
                        )
                        ui.Spacer(height=20)

                        # Input area - bottom fixed area
                        with ui.HStack(
                            height=60,
                            style={
                                "background_color": cl.color.black,
                                "padding": 5,
                                # "debug_color": cl.color("#00B4D811"),
                            },
                        ):
                            # Chat input field with Enter key handling
                            self._chat_input = ui.StringField(
                                height=40,
                                multiline=True,
                                name="chat-input",
                            )

                            # Add keyboard handler for Enter key
                            self._chat_input.set_key_pressed_fn(self._on_key_pressed)

                            # Add horizontal space
                            ui.Spacer(width=10)  # Adjust width as needed

                            # Send button (existing)
                            self._send_button = ui.Button(
                                "Send",
                                width=80,
                                height=40,
                                clicked_fn=self._send_message,
                                style={"background_color": cl.color("#00B4D8")},
                            )
                            self._voice_button = ui.Button(
                                name="voice",
                                width=40,
                                height=40,
                                clicked_fn=self._toggle_voice_input,
                                style={"background_color": cl.color("#00B4D8")},
                            )
                            self._upload_button = ui.Button(
                                name="upload",
                                width=40,
                                height=40,
                                clicked_fn=self._upload_file,
                                style={"background_color": cl.color("#00B4D8")},
                            )

        # Initialize chat interface after UI is built
        self.chat_interface = ChatInterface(
            self._chat_history, self._chat_input, self.llm_manager, self.scene_analyzer
        )

        # Initialize voice connection if API key is available
        self._initialize_voice_connection()

    def _setup_voice_callbacks(self):
        """Setup callbacks for voice interface"""
        self.voice_interface.set_ui_callbacks(
            on_transcript_update=self._on_transcript_update,
            on_status_update=self._on_voice_status_update,
            on_error=self._on_voice_error,
            on_audio_playback_start=self._on_audio_playback_start,
            on_audio_playback_end=self._on_audio_playback_end,
        )

    def _initialize_voice_connection(self):
        """Initialize voice connection if OpenAI API key is available"""
        # Get OpenAI API key from LLM manager settings
        carb.log_info(f"Initializing voice connection...")
        openai_config = self.llm_manager.providers.get("OpenAI GPT-4o", {})
        if openai_config:
            api_key_setting = openai_config.get("api_key_setting")
            if api_key_setting:
                api_key = self.llm_manager.settings.get_as_string(api_key_setting)
                if api_key:
                    # Initialize connection asynchronously
                    carb.log_info(
                        f"Initializing voice connection with API key: {api_key}"
                    )
                    asyncio.ensure_future(self._connect_voice_api(api_key))

    async def _connect_voice_api(self, api_key: str):
        """Connect to OpenAI Realtime API"""
        try:
            success = await self.voice_interface.initialize_connection(api_key, "alloy")
            self._voice_connected = success
            carb.log_info(
                f"Voice API connection: {'successful' if success else 'failed'}"
            )
        except Exception as e:
            carb.log_error(f"Failed to connect to voice API: {e}")
            self._voice_connected = False

    def _on_llm_changed(self, item_model, item=None):
        """Handle LLM provider change"""
        # ComboBox.model.add_item_changed_fn provides two arguments: model and item

        # Get the selected index from the model
        selected_index = item_model.get_item_value_model().get_value_as_int()
        providers = ["NVIDIA NIM", "OpenAI GPT-4o"]

        if 0 <= selected_index < len(providers):
            provider = providers[selected_index]
            self.llm_manager.set_provider(provider)
            print(f"Changed LLM provider to: {provider}")
        else:
            print(f"Invalid selection index: {selected_index}")

    def _save_api_key(self):
        """Save API key for current provider"""
        # Get the value directly from the StringField - this is correct
        api_key = self._api_key_field.model.get_value_as_string()
        # Get the selected index from the ComboBox
        selected_index = self._llm_combo.model.get_item_value_model().as_int
        providers = ["NVIDIA NIM", "OpenAI GPT-4o"]
        current_provider = providers[selected_index]

        # Log the results (for debugging only)
        print(f"API Key: {api_key}")

        # Save the key to the manager
        self.llm_manager.set_api_key(current_provider, api_key)
        print(f"API key saved for {current_provider}")

        # Voice connection is already initialized after UI build, so no need to reconnect here

    def _analyze_scene(self):
        """Analyze current USD scene"""
        analysis = self.scene_analyzer.analyze_current_scene()
        self._scene_info_label.text = analysis
        if self.chat_interface:
            self.chat_interface.update_scene_context(analysis)
        # Update voice interface with scene context
        if self.voice_interface:
            self.voice_interface.update_scene_context(analysis)
        self._on_ingest_document()

    def _export_chat(self):
        """Export chat history"""
        if self.chat_interface:
            self.chat_interface.export_history()

    def _export_analysis(self):
        """Export scene analysis"""
        analysis = self.scene_analyzer.get_detailed_analysis()
        carb.log_warn(f"Exporting scene analysis: {analysis}")
        # Create the directory if it doesn't exist
        import os

        export_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "scene_analysis",
        )
        os.makedirs(export_dir, exist_ok=True)

        # Generate a filename with timestamp
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(export_dir, f"scene_analysis_{timestamp}.md")

        # Write analysis to file - convert dictionary to formatted string if needed
        with open(filename, "w") as f:
            f.write(
                f"# Scene Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Convert dictionary to formatted string if analysis is a dict
            if isinstance(analysis, dict):
                formatted_analysis = "## Scene Analysis Details\n\n"
                for key, value in analysis.items():
                    formatted_analysis += f"### {key}\n{value}\n\n"
                f.write(formatted_analysis)
            else:
                # If it's already a string, write it directly
                f.write(str(analysis))

        print(f"Scene analysis exported to: {filename}")

    # Add these methods to the IvyverseWindow class
    def _on_key_pressed(self, key, modifier, consuming):
        """Handle keyboard events in the chat input field"""
        # Check if Enter key (key 13) is pressed without Shift
        if key == 51 and not (modifier & 1):  # 51 is Enter key
            self._send_message()
            return True  # Consume the event
        return False  # Let other handlers process the event

    def _on_ingest_document(self):
        """Handle document ingestion"""
        default_path = "/home/ubuntu/extsUser/ivyverse/context-aware-rag/data/OmniverseWarehouseSceneDescription.md"
        # Use default path since ingest_path UI element is not implemented
        file_path = default_path

        if file_path and os.path.exists(file_path):
            carb.log_warn(f"Attempting to ingest document: {file_path}")
            success = self.llm_manager.rag_manager.ingest_document(file_path)
            if success:
                # self._append_system_message(f"Document ingested: {os.path.basename(file_path)}")
                carb.log_warn(f"Document ingested: {os.path.basename(file_path)}")

            else:
                carb.log_warn("Failed to ingest document. Check console for details.")
        else:
            carb.log_warn("Invalid file path or file not found.")

    def _upload_file(self):
        """Handle audio file upload"""

        def _on_apply_input(file, directory):
            if directory and file:
                file_path = f"{directory}/{file}"
                # Process uploaded audio file
                asyncio.ensure_future(self._process_uploaded_audio(file_path))
            if self._input_filepicker:
                self._input_filepicker.hide()

        if not self._input_filepicker:
            self._input_filepicker = FilePickerDialog(
                "Select Audio File",
                click_apply_handler=_on_apply_input,
                file_extension_options=[
                    (".wav", "WAV Audio"),
                    (".mp3", "MP3 Audio"),
                    (".m4a", "M4A Audio"),
                    (".ogg", "OGG Audio"),
                    (".flac", "FLAC Audio"),
                ],
            )
        self._input_filepicker.show()

    def _toggle_voice_input(self):
        """Toggle voice recording on/off"""
        if not self._voice_connected:
            if self.chat_interface:
                timestamp = datetime.datetime.now().strftime("%H:%M %p")
                self.chat_interface._add_assistant_message(
                    "Voice feature not connected. Please save OpenAI API key first.",
                    timestamp,
                    "Voice System",
                )
            return

        if self._voice_recording:
            # Stop recording
            self._voice_recording = False
            self._voice_button.name = "voice"  # Change back to voice icon
            self.voice_interface.stop_recording()
        else:
            # Start recording
            self._voice_recording = True
            self._voice_response_mode = True  # Enable voice response
            self._voice_button.name = "audio-wave"  # Change to audio wave icon
            self.voice_interface.start_recording()

    async def _process_uploaded_audio(self, file_path: str):
        """Process uploaded audio file"""
        try:
            self._voice_response_mode = True  # Enable voice response for uploaded audio
            await self.voice_interface.process_audio_file(file_path)
        except Exception as e:
            carb.log_error(f"Error processing uploaded audio: {e}")
            if self.chat_interface:
                timestamp = datetime.datetime.now().strftime("%H:%M %p")
                self.chat_interface._add_assistant_message(
                    f"Error processing audio file: {str(e)}", timestamp, "Voice System"
                )

    # Voice interface callback methods
    def _on_transcript_update(self, transcript: str):
        """Handle transcript updates from voice interface"""
        if self._chat_input and transcript:
            # Update the input field with the transcription
            self._chat_input.model.set_value(transcript)
            carb.log_info(f"Transcript updated: {transcript}")

    def _on_voice_status_update(self, message: str, has_activity: bool):
        """Handle status updates from voice interface"""
        carb.log_info(f"Voice status: {message}")
        # Could update UI status indicator here if needed

    def _on_voice_error(self, error_message: str):
        """Handle voice interface errors"""
        carb.log_error(f"Voice error: {error_message}")
        # Reset voice recording state on error
        self._voice_recording = False
        self._voice_button.name = "voice"

        if self.chat_interface:
            # Add error message to chat
            timestamp = datetime.datetime.now().strftime("%H:%M %p")
            self.chat_interface._add_assistant_message(
                f"Voice Error: {error_message}", timestamp, "Voice System"
            )

    def _on_audio_playback_start(self):
        """Handle start of audio playback"""
        carb.log_info("Audio playback started")

    def _on_audio_playback_end(self):
        """Handle end of audio playback"""
        carb.log_info("Audio playback completed")
        # Reset voice response mode after playback
        self._voice_response_mode = False

    def _send_message(self):
        """Send message to LLM and optionally get speech response"""
        if self.chat_interface:
            # Get the message text
            message_text = self._chat_input.model.get_value_as_string()

            # If voice response mode is enabled, also get speech response
            if (
                self._voice_connected
                and self._voice_response_mode
                and message_text.strip()
            ):
                asyncio.ensure_future(
                    self.voice_interface.send_text_with_speech_response(message_text)
                )
            else:
                # Send regular chat message
                asyncio.ensure_future(self.chat_interface.send_message())

    def destroy(self):
        """Clean up resources"""
        # Clean up voice interface
        if self.voice_interface:
            self.voice_interface.cleanup()
            self.voice_interface = None

        self.llm_manager = None
        self.scene_analyzer = None
        self.chat_interface = None
        super().destroy()
