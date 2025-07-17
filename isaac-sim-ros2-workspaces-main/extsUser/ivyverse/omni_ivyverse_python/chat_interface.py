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
            avatar_text="V",
            icon_position="left",
        ),
        MessageType.THINKING: MessageConfig(
            background_color=0xFF196282,
            border_radius=8,
            avatar_bg_color=0xFF2C88D9,
            avatar_text="...",
            icon_position="right",
            show_source=False,
        ),
    }

    def __init__(self, parent_stack: ui.VStack):
        self.parent_stack = parent_stack

    def create_message(
        self,
        message: str,
        message_type: MessageType,
        timestamp: str = None,
        source: str = None,
        role_name: str = None,
    ) -> ui.ZStack:
        """Create a unified message bubble for any message type"""
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
                            self._create_content(
                                message, role_name, timestamp, source, config
                            )
                            ui.Spacer(width=10)
                        else:
                            ui.Spacer(width=10)
                            self._create_content(
                                message, role_name, timestamp, source, config
                            )
                            self._create_avatar(config)

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
    ) -> None:
        """Create message content area"""
        with ui.VStack(width=ui.Fraction(1)):
            # Header with role and timestamp
            if config.show_timestamp:
                with ui.HStack(height=24):
                    ui.Label(
                        role_name,
                        style={
                            "color": config.text_color,
                            "font_size": 12,
                            "font_weight": "bold",
                        },
                    )
                    ui.Spacer()
                    ui.Label(
                        timestamp,
                        style={"color": 0xFFCCCCCC, "font_size": 10},
                    )

            # Message text
            ui.Label(
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
            self.message_bubble = MessageBubble(self.chat_stack)

            # Welcome message
            self.add_message(
                message="Welcome to Ivyverse! I'm here to help you understand and analyze your USD scenes.",
                # message="こんにちは！Ivyverseへようこそ！USDシーンの理解と分析をお手伝いします。",
                message_type=MessageType.ASSISTANT,
                source="Initialization",
            )

    def add_message(
        self,
        message: str,
        message_type: MessageType,
        source: str = None,
        role_name: str = None,
    ):
        """Unified method to add any type of message with automatic timestamp generation"""
        # Generate timestamp here for consistency
        timestamp = datetime.datetime.now().strftime("%H:%M %p")

        # Create the message bubble
        container = self.message_bubble.create_message(
            message=message,
            message_type=message_type,
            timestamp=timestamp,
            source=source,
            role_name=role_name,
        )

        # Add to conversation history with ISO timestamp for data storage
        self.conversation_history.append(
            {
                "role": message_type.value,
                "content": message,
                "timestamp": datetime.datetime.now().isoformat(),
                "source": source,
            }
        )

        # Auto-scroll to bottom
        self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

        return container

    # Simplified convenience methods without timestamp parameters
    def add_user_message(self, message: str):
        """Add user message"""
        return self.add_message(message, MessageType.USER)

    def add_assistant_message(self, message: str, source: str = None):
        """Add assistant message"""
        return self.add_message(message, MessageType.ASSISTANT, source=source)

    def add_system_message(self, message: str, source: str = "System"):
        """Add system message"""
        return self.add_message(message, MessageType.SYSTEM, source=source)

    def add_error_message(self, message: str, source: str = "Error"):
        """Add error message"""
        return self.add_message(message, MessageType.ERROR, source=source)

    def add_voice_transcript(self, message: str):
        """Add voice transcript message"""
        return self.add_message(
            message, MessageType.VOICE_TRANSCRIPT, source="Voice Input"
        )

    def add_thinking_indicator(
        self, message: str = "I will now process your inquiry. Please wait..."
    ):
        """Add thinking indicator"""
        self.thinking_container = self.add_message(message, MessageType.THINKING)
        return self.thinking_container

    # def _add_user_message(self, message: str, timestamp: str):
    #     """Add a user message with enhanced styling using ZStack and Rectangle"""
    #     carb.log_error(f"Logging user message {message}")
    #     with self.chat_stack:
    #         # Create a container for the entire message
    #         with ui.ZStack(height=0):  # dynamic height
    #             # First layer: colored background rectangle
    #             ui.Rectangle(
    #                 style={
    #                     "background_color": 0xFF3A3A3A,  # User message background color
    #                     "border_radius": 8,  # Rounded corners
    #                     "border_color": 0xFF4F4F4F,  # Subtle border color
    #                     "border_width": 0,  # No border by default
    #                     # "debug_color": cl.color.red,
    #                 }
    #             )

    #             # Second layer: actual content
    #             with ui.VStack(style={"padding": 10}):  # Add padding to the content
    #                 with ui.HStack(height=0):  # Message layout
    #                     # User icon frame - on the left (opposite of assistant)
    #                     with ui.VStack(width=40):
    #                         with ui.Frame(
    #                             width=32,
    #                             height=32,
    #                             style={
    #                                 "background_color": 0xFF4F4F4F,
    #                                 "border_radius": 16,
    #                                 "margin": 4,
    #                                 # "debug_color": cl("#FF000055"),
    #                             },
    #                         ):
    #                             ui.Label(
    #                                 "U",
    #                                 alignment=ui.Alignment.CENTER,
    #                                 style={
    #                                     "color": 0xFFFFFFFF,
    #                                     "font_size": 16,
    #                                     # "debug_color": cl("#FF000055"),
    #                                 },
    #                             )

    #                     # Message container
    #                     with ui.VStack(width=ui.Fraction(1)):
    #                         # Header with timestamp
    #                         with ui.HStack(height=24):
    #                             ui.Label(
    #                                 "You",
    #                                 style={
    #                                     "color": 0xFFFFFFFF,
    #                                     "font_size": 12,
    #                                     "font_weight": "bold",
    #                                 },
    #                             )
    #                             ui.Spacer()
    #                             ui.Label(
    #                                 timestamp,
    #                                 style={"color": 0xFF808080, "font_size": 10},
    #                             )

    #                         # Message content text directly (no need for nested Frame)
    #                         ui.Label(
    #                             message,
    #                             word_wrap=True,
    #                             style={"color": 0xFFFFFFFF, "font_size": 13},
    #                         )

    #                     # Right spacing
    #                     ui.Spacer(width=10)

    #         # Force scroll to newest content
    #         self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

    # def _add_assistant_message(self, message: str, timestamp: str, source: str = None):
    #     """Add an assistant message with enhanced styling"""
    #     with self.chat_stack:
    #         # Create a container for the entire message
    #         with ui.ZStack(
    #             height=0,
    #             # style={"debug_color": cl("#FF000055")}
    #         ):  # dynamic height
    #             # First layer: colored background rectangle
    #             ui.Rectangle(
    #                 style={
    #                     "background_color": 0xFF196282,  # Background color
    #                     "border_radius": 8,  # Rounded corners
    #                     # "margin": 15,
    #                     "padding": 10,
    #                     "border_color": 0xFFFF5722,  # Add border color (orange in this example)
    #                     "border_width": 0,
    #                     # "padding": 10,
    #                     # "debug_color": cl("#FF000055"),
    #                 }
    #             )

    #             # Second layer: actual content
    #             with ui.VStack(style={"padding": 10}):  # Add padding to the content
    #                 with ui.HStack(height=0):  # Message layout
    #                     # Left spacing
    #                     ui.Spacer(width=10)

    #                     # Message container
    #                     with ui.VStack(width=ui.Fraction(1)):
    #                         # Header with timestamp
    #                         with ui.HStack(height=24):
    #                             ui.Label(
    #                                 "Assistant",
    #                                 style={
    #                                     "color": 0xFFFFFFFF,
    #                                     "font_size": 12,
    #                                     "font_weight": "bold",
    #                                 },
    #                             )
    #                             ui.Spacer()
    #                             ui.Label(
    #                                 timestamp,
    #                                 style={"color": 0xFFCCCCCC, "font_size": 10},
    #                             )

    #                         # Message content text
    #                         ui.Label(
    #                             message,
    #                             word_wrap=True,
    #                             style={"color": 0xFFFFFFFF, "font_size": 13},
    #                         )

    #                         # Source information if provided
    #                         if source:
    #                             with ui.HStack(
    #                                 height=20,
    #                                 # style={"margin_top": 5}
    #                             ):
    #                                 ui.Label(
    #                                     f"Source: {source}",
    #                                     style={"color": 0xFFCCCCCC, "font_size": 10},
    #                                 )

    #                     # Assistant icon frame
    #                     with ui.VStack(width=40):
    #                         with ui.Frame(
    #                             width=32,
    #                             height=32,
    #                             style={
    #                                 "background_color": 0xFF2C88D9,
    #                                 "border_radius": 16,
    #                                 "margin": 4,
    #                             },
    #                         ):
    #                             ui.Label(
    #                                 "A",
    #                                 alignment=ui.Alignment.CENTER,
    #                                 style={"color": 0xFFFFFFFF, "font_size": 16},
    #                             )

    #                     ui.Spacer(width=10)

    #         # Force scroll to newest content
    #         self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

    # def _add_thinking_indicator(self):
    #     """Add a 'thinking' indicator when the assistant is processing a request"""
    #     with self.chat_stack:
    #         # Store reference to the entire container for later removal
    #         self.thinking_container = ui.ZStack(
    #             height=0
    #         )  # Use ZStack for consistent styling

    #         with self.thinking_container:
    #             # First layer: colored background rectangle
    #             ui.Rectangle(
    #                 style={
    #                     "background_color": 0xFF196282,  # Background color
    #                     "border_radius": 8,  # Rounded corners
    #                 }
    #             )

    #             # Second layer: actual content
    #             with ui.VStack(style={"padding": 10}):
    #                 with ui.HStack(height=0):
    #                     # Left spacing
    #                     ui.Spacer(width=10)

    #                     # Processing message
    #                     with ui.VStack(width=ui.Fraction(1)):
    #                         # Header with timestamp
    #                         with ui.HStack(height=24):
    #                             ui.Label(
    #                                 "Assistant",
    #                                 style={
    #                                     "color": 0xFFFFFFFF,
    #                                     "font_size": 12,
    #                                     "font_weight": "bold",
    #                                 },
    #                             )
    #                             ui.Spacer()
    #                             ui.Label(
    #                                 datetime.datetime.now().strftime("%H:%M %p"),
    #                                 style={"color": 0xFF808080, "font_size": 10},
    #                             )

    #                         # Processing label
    #                         self.processing_label = ui.Label(
    #                             "I will now process your inquiry. Please wait...",
    #                             # "処理中でお問い合わせを処理します。お待ちください...",
    #                             style={"color": 0xFFFFFFFF, "font_size": 13},
    #                         )

    #                     # Assistant icon frame
    #                     with ui.VStack(width=40):
    #                         with ui.Frame(
    #                             width=32,
    #                             height=32,
    #                             style={
    #                                 "background_color": 0xFF2C88D9,
    #                                 "border_radius": 16,
    #                                 "margin": 4,
    #                             },
    #                         ):
    #                             ui.Label(
    #                                 "A",
    #                                 alignment=ui.Alignment.CENTER,
    #                                 style={"color": 0xFFFFFFFF, "font_size": 16},
    #                             )

    #                     ui.Spacer(width=10)

    #         # Force scroll to newest content
    #         self.chat_history_frame.scroll_y = self.chat_history_frame.scroll_y_max

    #         return self.processing_label

    def _remove_thinking_indicator(self):
        """Remove the 'thinking' indicator"""
        if hasattr(self, "thinking_container") and self.thinking_container:
            # Remove the entire container from the UI tree
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
            "Scene context updated. I now have the latest information about your USD scene.",
            # "シーンコンテキストが更新されました。USDシーンに関する最新情報を取得しました。",
            "Scene Analysis",
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
                f"Chat history exported to: {filepath}", "System"
            )
        except Exception as e:
            self.add_assistant_message(
                f"Error exporting chat history: {str(e)}", "System Error"
            )

    # Add this method to the ChatInterface class
    # def display_system_message(self, message):
    #     """Display a system message in the chat"""
    #     # Create a frame for the system message with special styling
    #     with self.chat_history:
    #         with ui.ZStack():
    #             ui.Rectangle(
    #                 style={
    #                     "background_color": COLORS["surface"],
    #                     "border_radius": 8,
    #                     "border_color": COLORS["accent"],
    #                     "border_width": 1,
    #                 }
    #             )
    #             with ui.VStack(style={"padding": 10}):
    #                 ui.Label(
    #                     message,
    #                     word_wrap=True,
    #                     style={
    #                         "color": COLORS["accent"],
    #                         "font_size": 14,
    #                     },
    #                 )
    #                 ui.Label(
    #                     "System",
    #                     style={
    #                         "color": COLORS["text_secondary"],
    #                         "font_size": 10,
    #                     },
    #                 )
