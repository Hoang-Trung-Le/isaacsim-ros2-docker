import omni.ui as ui
import carb
import asyncio
import json
import datetime
from typing import List, Dict, Any, Optional
from omni.ui import color as cl
from enum import Enum
from dataclasses import dataclass


class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"
    VOICE_TRANSCRIPT = "voice_transcript"
    THINKING = "thinking"


@dataclass
class MessageConfig:
    background_color: int
    border_radius: int
    border_color: int = 0x00000000
    border_width: int = 0
    avatar_bg_color: int = 0xFF4F4F4F
    avatar_text: str = "A"
    text_color: int = 0xFFFFFFFF
    icon_position: str = "right"  # "left" or "right"
    show_timestamp: bool = True
    show_source: bool = True


class MessageBubble:
    """Unified message bubble component for all message types"""

    # Message type configurations
    CONFIGS = {
        MessageType.USER: MessageConfig(
            background_color=0xFF3A3A3A,
            border_radius=8,
            avatar_bg_color=0xFF4F4F4F,
            avatar_text="U",
            icon_position="left",
        ),
        MessageType.ASSISTANT: MessageConfig(
            background_color=0xFF196282,
            border_radius=8,
            avatar_bg_color=0xFF2C88D9,
            avatar_text="A",
            icon_position="right",
        ),
        MessageType.SYSTEM: MessageConfig(
            background_color=0xFF2D4A22,
            border_radius=6,
            avatar_bg_color=0xFF4CAF50,
            avatar_text="S",
            icon_position="right",
        ),
        MessageType.ERROR: MessageConfig(
            background_color=0xFF4A1F1F,
            border_radius=6,
            avatar_bg_color=0xFFE53E3E,
            avatar_text="!",
            icon_position="right",
        ),
        MessageType.VOICE_TRANSCRIPT: MessageConfig(
            background_color=0xFF2D3748,
            border_radius=6,
            avatar_bg_color=0xFF805AD5,
            avatar_text="A",
            icon_position="left",
        ),
        MessageType.THINKING: MessageConfig(
            background_color=0xFF196282,
            border_radius=8,
            avatar_bg_color=0xFF2C88D9,
            avatar_text="A",
            icon_position="right",
            show_source=False,
        ),
    }

    def __init__(
        self, parent_stack: ui.VStack, conversation_history: List[Dict[str, Any]]
    ):
        self.parent_stack = parent_stack
        self.conversation_history = (
            conversation_history  # Reference to ChatInterface history
        )
        # Professional practice: Single live transcript state management
        self._message_data = None  # {id, label, text_buffer, timestamp, container}

    def create_message(
        self,
        message: str,
        message_type: MessageType,
        timestamp: str = None,
        source: str = None,
        role_name: str = None,
        is_done: bool = True,
    ) -> ui.ZStack:
        """Create a unified message bubble for any message type"""

        # Initialize on first call
        if self._message_data is None:
            import uuid

            message_id = f"{message_type.value}_{uuid.uuid4().hex[:8]}"

            config = self.CONFIGS[message_type]
            if not timestamp:
                timestamp = datetime.datetime.now().strftime("%H:%M %p")
            if not role_name:
                role_name = message_type.value.title()

            with self.parent_stack:
                container = ui.ZStack(height=0)

                with container:
                    # Background rectangle
                    ui.Rectangle(
                        style={
                            "background_color": config.background_color,
                            "border_radius": config.border_radius,
                            "border_color": config.border_color,
                            "border_width": config.border_width,
                        }
                    )

                    # Content layout
                    with ui.VStack(style={"padding": 10}):
                        with ui.HStack(height=0):
                            if config.icon_position == "left":
                                self._create_avatar(config)
                                message_label = self._create_content(
                                    message,
                                    role_name,
                                    timestamp,
                                    source,
                                    config,
                                )
                                ui.Spacer(width=10)
                            else:
                                ui.Spacer(width=10)
                                message_label = self._create_content(
                                    message,
                                    role_name,
                                    timestamp,
                                    source,
                                    config,
                                )
                                self._create_avatar(config)

                self._message_data = {
                    "id": message_id,
                    "label": message_label,
                    "text_buffer": message,
                    "timestamp": timestamp,
                }

        if self._message_data and not is_done:
            self._message_data["text_buffer"] += message
            if self._message_data["label"] and hasattr(
                self._message_data["label"], "text"
            ):
                self._message_data["label"].text = self._message_data["text_buffer"]

        if self._message_data and is_done:
            self.conversation_history.append(
                {
                    "role": message_type.value,
                    "content": self._message_data["text_buffer"],
                    "timestamp": self._message_data["timestamp"],
                    "source": source,
                    "message_id": self._message_data["id"],
                }
            )
            state_to_cleanup = self._message_data
            self._message_data = None
            asyncio.ensure_future(self._cleanup_after_delay(state_to_cleanup, 2.0))
        return container

    def _create_avatar(self, config: MessageConfig) -> None:
        """Create avatar icon"""
        with ui.VStack(width=40):
            with ui.Frame(
                width=32,
                height=32,
                style={
                    "background_color": config.avatar_bg_color,
                    "border_radius": 16,
                    "margin": 4,
                },
            ):
                ui.Label(
                    config.avatar_text,
                    alignment=ui.Alignment.CENTER,
                    style={
                        "color": config.text_color,
                        "font_size": 16,
                    },
                )

    def _create_content(
        self,
        message: str,
        role_name: str,
        timestamp: str,
        source: str,
        config: MessageConfig,
    ) -> ui.Label:
        """Create message content area"""
        message_label = None

        with ui.VStack(width=ui.Fraction(1)):
            # Header with role and timestamp
            if config.show_timestamp:
                with ui.HStack(height=24):
                    ui.Label(
                        role_name,
                        style={
                            "color": config.text_color,
                            "font_size": 12,
                        },
                    )
                    ui.Spacer()
                    ui.Label(
                        timestamp,
                        style={"color": 0xFFCCCCCC, "font_size": 10},
                    )

            # Message text - store reference for live updates
            message_label = ui.Label(
                message,
                word_wrap=True,
                style={"color": config.text_color, "font_size": 13},
            )

            # Source information
            if config.show_source and source:
                ui.Label(
                    f"Source: {source}",
                    style={"color": 0xFFCCCCCC, "font_size": 10},
                )

        return message_label

    async def _cleanup_after_delay(self, state: dict, delay: float):
        """Professional cleanup with delay"""
        await asyncio.sleep(delay)
        # State is already copied, safe to cleanup
        carb.log_info(f"Cleaned up live transcript: {state['id']}")


class ChatInterface:
    """Manages the chat interface and conversation flow similar to modern chat applications"""

    def __init__(self, chat_history_frame, chat_input, llm_manager, scene_analyzer):
        self.chat_history_frame = chat_history_frame
        self.chat_input = chat_input
        self.llm_manager = llm_manager
        self.scene_analyzer = scene_analyzer
        self.conversation_history = []
        self.scene_context = ""
        self.thinking_container = None
        self._build_chat_ui()

    def _build_chat_ui(self):
        """Build the chat UI within the history frame"""
        with self.chat_history_frame:
            self.chat_stack = ui.VStack()
            # Pass conversation history reference for professional state management
            self.message_bubble = MessageBubble(
                self.chat_stack, self.conversation_history
            )

            # Welcome message
            self.add_assistant_message(
                message="Welcome to Ivyverse! I'm here to help you understand and analyze your USD scenes.",
                # message="こんにちは！Ivyverseへようこそ！USDシーンの理解と分析をお手伝いします。",
                source="Initialization",
            )

    def add_message(
        self,
        message: str,
        message_type: MessageType,
        source: str = None,
        is_done: bool = True,
    ):
        """Unified method to add any type of message with automatic timestamp generation"""

        # Create the message bubble
        self.message_bubble.create_message(
            message=message,
            message_type=message_type,
            source=source,
            is_done=is_done,
        )

        # Auto-scroll to bottom
        self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

    def add_live_transcript(
        self, delta_text: str, is_done: bool = False, source="Voice Transcript"
    ):
        """
        Professional single-entry point for live transcript handling
        Call this method from external voice handler with each delta and completion flag
        """
        return self.add_message(
            delta_text, MessageType.VOICE_TRANSCRIPT, is_done=is_done, source=source
        )

    # Simplified convenience methods without timestamp parameters
    def add_user_message(self, message: str):
        return self.add_message(message, MessageType.USER)

    def add_assistant_message(self, message: str, source: str = None):
        return self.add_message(message, MessageType.ASSISTANT, source=source)

    def add_system_message(self, message: str, source: str = "System"):
        return self.add_message(message, MessageType.SYSTEM, source=source)

    def add_error_message(self, message: str, source: str = "Error"):
        return self.add_message(message, MessageType.ERROR, source=source)

    def add_thinking_indicator(
        self, message: str = "I will now process your inquiry. Please wait..."
    ):
        self.thinking_container = self.add_message(message, MessageType.THINKING)
        return self.thinking_container

    def _remove_thinking_indicator(self):
        if hasattr(self, "thinking_container") and self.thinking_container:
            self.thinking_container.destroy()
            self.thinking_container = None

    async def send_message(self):
        """Send user message to LLM and get response"""
        user_message = self.chat_input.model.get_value_as_string()

        if not user_message.strip():
            return

        # Clear input
        self.chat_input.model.set_value("")

        # Add user message to UI
        self.add_user_message(user_message)
        carb.log_warn(f"user message {user_message}")

        # Check for direct commands first
        direct_response = self._handle_direct_commands(user_message)

        if direct_response:
            self.add_assistant_message(direct_response, "Direct Command")
            return

        # Prepare messages for LLM
        messages = self._prepare_messages(user_message)

        # Add thinking indicator
        self.add_thinking_indicator()

        # Ensure chat scrolls to bottom - set scroll_y to maximum position
        self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

        carb.log_warn("Pre-Response!")
        # Query LLM
        response = await self.llm_manager.query(messages)
        carb.log_warn(f"Response! {messages}")

        # Remove thinking indicator
        self._remove_thinking_indicator()

        # Add response
        self.add_assistant_message(response, "LLM Response")

        # Ensure chat scrolls to bottom again
        self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

        # Handle any scene-related queries
        await self._handle_scene_queries(user_message, response)

    def _handle_direct_commands(self, user_message: str) -> str:
        """Handle direct commands that don't need LLM"""
        user_message_lower = user_message.lower().strip()

        if user_message_lower == "overview":
            return self.scene_analyzer.analyze_current_scene()

        elif user_message_lower == "objects":
            objects = self.scene_analyzer.get_objects_list()
            summary = "Objects in the scene:\n"

            for category, items in objects.items():
                if items:
                    summary += f"\n{category.title()} ({len(items)}):\n"
                    for item in items[:10]:
                        if category == "meshes":
                            summary += f"  - {item['path']} ({item['vertex_count']} vertices, {item.get('face_count', 0)} faces)\n"
                        elif category == "lights":
                            summary += f"  - {item['path']} ({item['type']})\n"
                        else:
                            summary += f"  - {item['path']}\n"
                    if len(items) > 10:
                        summary += f"  ... and {len(items) - 10} more\n"

            return summary

        elif user_message_lower == "lights":
            lights = self.scene_analyzer._get_lights_list()
            if lights:
                light_list = "\n".join([f"- {l['path']} ({l['type']})" for l in lights])
                return f"Found {len(lights)} lights:\n{light_list}"
            else:
                return "No lights found in the scene."

        elif user_message_lower == "meshes":
            meshes = self.scene_analyzer._get_meshes_list()
            if meshes:
                mesh_list = "\n".join(
                    [
                        f"- {m['path']} ({m['vertex_count']} vertices, {m.get('face_count', 0)} faces)"
                        for m in meshes[:20]
                    ]
                )
                return f"Found {len(meshes)} meshes:\n{mesh_list}"
            else:
                return "No meshes found in the scene."

        elif user_message_lower == "materials":
            materials = self.scene_analyzer._get_materials_list()
            if materials:
                material_list = "\n".join(
                    [
                        f"- {m['path']} ({m.get('type', 'Unknown')})"
                        for m in materials[:30]
                    ]
                )
                return f"Found {len(materials)} materials:\n{material_list}"
            else:
                return "No materials found in the scene."

        elif user_message_lower == "hierarchy":
            hierarchy = self.scene_analyzer.get_hierarchy()
            return json.dumps(hierarchy, indent=2)

        elif user_message_lower.startswith("search "):
            query = user_message[7:].strip()
            results = self.scene_analyzer.search_prims(query)
            if results:
                return f"Found {len(results)} matching prims:\n" + "\n".join(
                    results[:20]
                )
            else:
                return "No prims found matching your search."

        elif user_message_lower.startswith("prim "):
            prim_path = user_message[5:].strip()
            if not prim_path.startswith("/"):
                prim_path = "/" + prim_path
            info = self.scene_analyzer.get_prim_info(prim_path)
            return json.dumps(info, indent=2)

        return None

    def _prepare_messages(self, user_message: str) -> List[Dict[str, str]]:
        """Prepare messages for LLM including context"""
        messages = []

        # System prompt with detailed scene context
        system_prompt = self.llm_manager.get_system_prompt()
        if self.scene_context:
            system_prompt += f"\n\nCurrent Scene Context:\n{self.scene_context}"

        # Add enhanced instructions for better responses
        system_prompt += """
When answering questions about scene contents:
- Always provide exact counts when available
- List specific objects with their paths
- Describe the purpose and function of objects
- Be precise about object types and properties
"""

        messages.append({"role": "system", "content": system_prompt})

        # Add recent conversation history (last 10 messages)
        for msg in self.conversation_history[-10:]:
            if msg["role"] in ["user", "assistant"]:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _handle_scene_queries(self, user_message: str, response: str):
        """Handle scene-specific queries and commands"""
        user_message_lower = user_message.lower()

        # Check for prim-specific queries
        if "prim" in user_message_lower or "path" in user_message_lower:
            # Extract path if mentioned
            import re

            path_match = re.search(r'["\']([^"\']+)["\']', user_message)
            if path_match:
                prim_path = path_match.group(1)
                prim_info = self.scene_analyzer.get_prim_info(prim_path)

                # Add additional context if needed
                if not prim_info.get("error"):
                    info_str = json.dumps(prim_info, indent=2)
                    self.add_assistant_message(
                        f"Additional prim details:\n```json\n{info_str}\n```",
                        "Scene Analysis",
                    )

        # Check for search queries
        elif "search" in user_message_lower or "find" in user_message_lower:
            # Extract search term
            words = user_message.split()
            if len(words) > 1:
                search_term = words[-1]
                results = self.scene_analyzer.search_prims(search_term)

                if results:
                    result_str = "\n".join(results[:10])  # Show first 10 results
                    self.add_assistant_message(
                        f"Found {len(results)} matching prims:\n{result_str}",
                        "Search Results",
                    )

    def update_scene_context(self, context: str):
        """Update the scene context for LLM"""
        self.scene_context = context

        # Add detailed object information to context
        objects = self.scene_analyzer.get_objects_list()

        object_details = "\n\nDetailed Object Information:"

        # Add mesh details
        if objects["meshes"]:
            object_details += f"\n\nMeshes ({len(objects['meshes'])}):"
            for mesh in objects["meshes"][:10]:
                object_details += (
                    f"\n- {mesh['path']} ({mesh['vertex_count']} vertices)"
                )

        # Add light details
        if objects["lights"]:
            object_details += f"\n\nLights ({len(objects['lights'])}):"
            for light in objects["lights"]:
                object_details += f"\n- {light['path']} ({light['type']})"

        # Add material details
        if objects["materials"]:
            object_details += f"\n\nMaterials ({len(objects['materials'])}):"
            for material in objects["materials"][:10]:
                object_details += f"\n- {material['path']} ({material['type']})"

        self.scene_context = context + object_details
        self.add_assistant_message(
            message="Scene context updated. I now have the latest information about your USD scene.",
            # message="シーンコンテキストが更新されました。USDシーンに関する最新情報を取得しました。",
            source="Scene Analysis",
        )

    def export_history(self, filepath: str = None):
        """Export conversation history to file"""
        if not filepath:
            filepath = f"ivyverse_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data = {
            "conversation": self.conversation_history,
            "scene_context": self.scene_context,
            "export_time": datetime.datetime.now().isoformat(),
        }

        try:
            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2)
            self.add_assistant_message(
                message=f"Chat history exported to: {filepath}",
                source="System",
            )
        except Exception as e:
            self.add_assistant_message(
                message=f"Error exporting chat history: {str(e)}",
                source="System Error",
            )
