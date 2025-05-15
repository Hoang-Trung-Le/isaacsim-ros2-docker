import omni.ui as ui
import asyncio
import json
import datetime
from typing import List, Dict, Any, Optional
class ChatInterface:
    """Manages the chat interface and conversation flow"""
    
    def __init__(self, chat_history_frame, chat_input, llm_manager, scene_analyzer):
        self.chat_history_frame = chat_history_frame
        self.chat_input = chat_input
        self.llm_manager = llm_manager
        self.scene_analyzer = scene_analyzer
        self.conversation_history = []
        self.scene_context = ""
        self._build_chat_ui()
    
    def _build_chat_ui(self):
        """Build the chat UI within the history frame"""
        with self.chat_history_frame:
            self.chat_stack = ui.VStack(spacing=10)
            with self.chat_stack:
                # Welcome message
                self._add_message("Welcome to Ivyverse! I'm here to help you understand and analyze your USD scenes.", "assistant")
    
    def _add_message(self, message: str, role: str):
        """Add a message to the chat UI"""
        with self.chat_stack:
            with ui.HStack(height=0):
                if role == "user":
                    ui.Spacer(width=50)
                    with ui.Frame(style={
                        "background_color": 0xFF333333,
                        "border_radius": 10,
                        "padding": 10
                    }):
                        ui.Label(message, word_wrap=True, style={"color": 0xFFFFFFFF})
                else:
                    with ui.Frame(style={
                        "background_color": 0xFF0084FF,
                        "border_radius": 10,
                        "padding": 10
                    }):
                        ui.Label(message, word_wrap=True, style={"color": 0xFFFFFFFF})
                    ui.Spacer(width=50)
        
        # Add to conversation history
        self.conversation_history.append({
            "role": role,
            "content": message,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    async def send_message(self):
        """Send user message to LLM and get response"""
        user_message = self.chat_input.model.get_value_as_string()
        
        if not user_message.strip():
            return
        
        # Clear input
        self.chat_input.model.set_value("")
        
        # Add user message to UI
        self._add_message(user_message, "user")
        
        # Check for direct commands first
        direct_response = self._handle_direct_commands(user_message)
        
        if direct_response:
            self._add_message(direct_response, "assistant")
            return
        
        # Prepare messages for LLM
        messages = self._prepare_messages(user_message)
        
        # Add loading indicator
        loading_label = None
        with self.chat_stack:
            with ui.HStack(height=0):
                with ui.Frame(style={
                    "background_color": 0xFF0084FF,
                    "border_radius": 10,
                    "padding": 10
                }):
                    loading_label = ui.Label("Thinking...", word_wrap=True, style={"color": 0xFFFFFFFF})
                ui.Spacer(width=50)
        
        # Query LLM
        response = await self.llm_manager.query(messages)
        
        # Remove loading indicator
        if loading_label:
            loading_label.visible = False
        
        # Add response
        self._add_message(response, "assistant")
        
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
                mesh_list = "\n".join([f"- {m['path']} ({m['vertex_count']} vertices, {m.get('face_count', 0)} faces)" 
                                     for m in meshes[:20]])
                return f"Found {len(meshes)} meshes:\n{mesh_list}"
            else:
                return "No meshes found in the scene."
                
        elif user_message_lower == "materials":
            materials = self.scene_analyzer._get_materials_list()
            if materials:
                material_list = "\n".join([f"- {m['path']} ({m.get('type', 'Unknown')})" for m in materials[:30]])
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
                return f"Found {len(results)} matching prims:\n" + "\n".join(results[:20])
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
                    self._add_message(f"Additional prim details:\n```json\n{info_str}\n```", "assistant")
        
        # Check for search queries
        elif "search" in user_message_lower or "find" in user_message_lower:
            # Extract search term
            words = user_message.split()
            if len(words) > 1:
                search_term = words[-1]
                results = self.scene_analyzer.search_prims(search_term)
                
                if results:
                    result_str = "\n".join(results[:10])  # Show first 10 results
                    self._add_message(f"Found {len(results)} matching prims:\n{result_str}", "assistant")
    
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
                object_details += f"\n- {mesh['path']} ({mesh['vertex_count']} vertices)"
                
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
        self._add_message("Scene context updated. I now have the latest information about your USD scene.", "assistant")
    
    def export_history(self, filepath: str = None):
        """Export conversation history to file"""
        if not filepath:
            filepath = f"ivyverse_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "conversation": self.conversation_history,
            "scene_context": self.scene_context,
            "export_time": datetime.datetime.now().isoformat()
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            self._add_message(f"Chat history exported to: {filepath}", "assistant")
        except Exception as e:
            self._add_message(f"Error exporting chat history: {str(e)}", "assistant")
