import omni.ui as ui
import asyncio
from .llm_manager import LLMManager
from .scene_analyzer import SceneAnalyzer
from .chat_interface import ChatInterface
class IvyverseWindow(ui.Window):
    """Main window for Ivyverse extension"""
    
    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)
        self.frame.set_build_fn(self._build_window)
        self.llm_manager = LLMManager()
        self.scene_analyzer = SceneAnalyzer()
        self.chat_interface = None
        
    def _build_window(self):
        with self.frame:
            with ui.VStack(spacing=10, height=0):
                # Header
                with ui.HStack(height=80):
                    ui.Label("Ivyverse", style={"font_size": 24, "color": 0xFF00B4D8})
                    ui.Label("USD Scene Copilot", style={"font_size": 16, "color": 0xFF909090})
                
                # Configuration Section
                with ui.CollapsableFrame("Configuration", height=100):
                    with ui.VStack(spacing=5):
                        # LLM Selection
                        with ui.HStack(height=30):
                            ui.Label("LLM Provider:", width=100)
                            self._llm_combo = ui.ComboBox(
                                model=ui.SimpleStringModel(["NVIDIA NIM", "OpenAI GPT-4o"]),
                                width=200
                            )
                            self._llm_combo.model.add_item_changed_fn(self._on_llm_changed)
                        
                        # API Key Input
                        with ui.HStack(height=30):
                            ui.Label("API Key:", width=100)
                            self._api_key_field = ui.PasswordField(width=300)
                            self._save_button = ui.Button("Save", width=80, clicked_fn=self._save_api_key)
                
                # Scene Information
                with ui.CollapsableFrame("Scene Information", height=150):
                    with ui.VStack(spacing=5):
                        self._scene_info_label = ui.Label("No scene loaded", word_wrap=True)
                        ui.Button("Analyze Current Scene", height=30, clicked_fn=self._analyze_scene)
                
                # Chat Interface
                with ui.CollapsableFrame("Chat", collapsed=False):
                    with ui.VStack(spacing=5):
                        # Chat history
                        self._chat_history = ui.ScrollingFrame(height=400)
                        
                        # Input area
                        with ui.HStack(height=60):
                            self._chat_input = ui.MultiField(height=50)
                            self._send_button = ui.Button(
                                "Send", 
                                width=80, 
                                height=50,
                                clicked_fn=self._send_message
                            )
                
                # Export Options
                with ui.CollapsableFrame("Export Options", height=60):
                    with ui.HStack(spacing=10):
                        ui.Button("Export Chat History", clicked_fn=self._export_chat)
                        ui.Button("Export Scene Analysis", clicked_fn=self._export_analysis)
        
        # Initialize chat interface after UI is built
        self.chat_interface = ChatInterface(
            self._chat_history,
            self._chat_input,
            self.llm_manager,
            self.scene_analyzer
        )
    
    def _on_llm_changed(self, model, item):
        """Handle LLM provider change"""
        provider = model.get_item_value_model(item).as_string
        self.llm_manager.set_provider(provider)
        print(f"Changed LLM provider to: {provider}")
    
    def _save_api_key(self):
        """Save API key for current provider"""
        api_key = self._api_key_field.model.as_string
        current_provider = self._llm_combo.model.get_item_value_model().as_string
        self.llm_manager.set_api_key(current_provider, api_key)
        print(f"API key saved for {current_provider}")
    
    def _analyze_scene(self):
        """Analyze current USD scene"""
        analysis = self.scene_analyzer.analyze_current_scene()
        self._scene_info_label.text = analysis
        if self.chat_interface:
            self.chat_interface.update_scene_context(analysis)
    
    def _send_message(self):
        """Send message to LLM"""
        if self.chat_interface:
            asyncio.ensure_future(self.chat_interface.send_message())
    
    def _export_chat(self):
        """Export chat history"""
        if self.chat_interface:
            self.chat_interface.export_history()
    
    def _export_analysis(self):
        """Export scene analysis"""
        analysis = self.scene_analyzer.get_detailed_analysis()
        # TODO: Implement export functionality
        print("Exporting scene analysis...")
    
    def destroy(self):
        """Clean up resources"""
        self.llm_manager = None
        self.scene_analyzer = None
        self.chat_interface = None
        super().destroy()
