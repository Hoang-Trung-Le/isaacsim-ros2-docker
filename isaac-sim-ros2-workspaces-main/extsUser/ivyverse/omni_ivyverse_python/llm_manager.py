import carb
import aiohttp
import json
import re
from typing import Dict, Any, Optional, List
from .rag_manager import RAGManager  # Assuming RAGManager is in the same directory
 
class LLMManager:
    """Manages LLM providers and API calls"""

    def __init__(self):
        self.settings = carb.settings.get_settings()
        self.current_provider = "OpenAI GPT-4o"
        self.providers = {
            "NVIDIA NIM": {
                "url": "https://api.nvidia.com/v1/chat/completions",
                "model": "nvidia/llama3-70b-instruct",
                "api_key_setting": "/persistent/exts/omni.ivyverse/nim_api_key"
            },
            "OpenAI GPT-4o": {
                "url": "https://api.openai.com/v1/chat/completions",
                "model": "gpt-4o-mini",
                "api_key_setting": "/persistent/exts/omni.ivyverse/openai_api_key"
            }
        }
        self.rag_manager = RAGManager()
        self.use_rag = True  # Default to not using RAG

    def _detect_language(self, text: str) -> str:
        """Detect if the text contains Japanese characters"""
        # Check for Japanese characters (Hiragana, Katakana, Kanji)
        japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')
        if japanese_pattern.search(text):
            return "Japanese"
        return "English"

    def _get_language_specific_system_prompt(self, detected_language: str) -> str:
        """Get system prompt with language-specific instructions"""
        base_prompt = """You are an industrial USD scene assistant for NVIDIA Omniverse.
You help users understand and analyze their 3D scenes by answering questions about:
- Scene hierarchy and structure
- Prim properties and attributes
- Materials and shaders
- Transformations and relationships
- Performance optimization
- Best practices for USD workflows

Be technical and precise, but also explain complex concepts clearly.
Use the provided scene context to give accurate, helpful answers."""

        if detected_language == "Japanese":
            language_instruction = """

IMPORTANT: The user is communicating in Japanese. Please respond in natural, polite Japanese (です/ます調). 
When explaining technical terms:
- Use Japanese translations when appropriate
- Include English technical terms in parentheses when necessary
- Maintain technical accuracy while being accessible in Japanese

日本語で回答してください。技術的な内容も分かりやすく日本語で説明し、必要に応じて英語の専門用語を併記してください。"""
        else:
            language_instruction = """

Respond in clear, professional English."""

        return base_prompt + language_instruction
        
    async def query(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
        """Send query to current LLM provider or RAG system if enabled"""
        carb.log_warn(f"Query started with provider: {self.current_provider}, RAG enabled: {self.use_rag}")
        
        # Detect language from the user's message
        user_message = ""
        if len(messages) > 0 and messages[-1]["role"] == "user":
            user_message = messages[-1]["content"]
            detected_language = self._detect_language(user_message)
            carb.log_info(f"Detected language: {detected_language}")
        else:
            detected_language = "English"

        # If RAG is enabled and this is a user query, try RAG first
        if self.use_rag and len(messages) > 1 and messages[-1]["role"] == "user":
            user_query = messages[-1]["content"]
            carb.log_warn(f"Attempting RAG query with: '{user_query[:50]}...'")
            try:
                rag_response = await self.rag_manager.query_rag(user_query, detected_language)
                carb.log_warn(f"RAG response received: {rag_response}, length: {len(rag_response) if rag_response else 0}")

                if rag_response and not rag_response.startswith("Error:"):
                    # Append RAG context to the system message or create a new one
                    has_system = any(msg["role"] == "system" for msg in messages)
                    if has_system:
                        for i, msg in enumerate(messages):
                            if msg["role"] == "system":
                                carb.log_warn("Adding RAG context to existing system message")
                                messages[i]["content"] += "\n\nAdditional context from documents:\n" + rag_response
                                break
                    else:
                        carb.log_warn("Creating new system message with RAG context")
                        messages.insert(0, {
                            "role": "system",
                            "content": "Additional context from documents:\n" + rag_response
                        })
                else:
                    carb.log_warn(f"RAG returned error or empty response: {rag_response[:100] if rag_response else 'None'}")
            except Exception as e:
                carb.log_error(f"RAG query failed: {str(e)}, falling back to standard LLM query")

        # Update or add system message with language-specific instructions
        language_system_prompt = self._get_language_specific_system_prompt(detected_language)
        
        # Find existing system message or add new one
        has_system = any(msg["role"] == "system" for msg in messages)
        if has_system:
            for i, msg in enumerate(messages):
                if msg["role"] == "system":
                    # Preserve any RAG context that was added above
                    if "\n\nAdditional context from documents:\n" in msg["content"]:
                        rag_context = msg["content"].split("\n\nAdditional context from documents:\n", 1)[1]
                        messages[i]["content"] = language_system_prompt + "\n\nAdditional context from documents:\n" + rag_context
                    else:
                        messages[i]["content"] = language_system_prompt
                    break
        else:
            messages.insert(0, {
                "role": "system",
                "content": language_system_prompt
            })
                
        # Continue with standard LLM query
        provider_config = self.providers[self.current_provider]
        api_key = self.settings.get_as_string(provider_config["api_key_setting"])

        if not api_key:
            carb.log_error(f"No API key configured for {self.current_provider}")
            return "Error: No API key configured for " + self.current_provider

        carb.log_warn(f"Preparing LLM query with model: {provider_config['model']}")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": provider_config["model"],
            "messages": messages,
            "temperature": temperature
        }
        
        message_count = len(messages)
        token_estimate = sum(len(msg["content"].split()) * 1.3 for msg in messages)
        carb.log_warn(f"Sending query with {message_count} messages, approx {int(token_estimate)} tokens")

        try:
            carb.log_warn(f"Sending request to: {provider_config['url']}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    provider_config["url"],
                    headers=headers,
                    json=data
                ) as response:
                    carb.log_warn(f"Response received, status: {response.status}")
                    result = await response.json()

                    if response.status == 200:
                        response_text = result["choices"][0]["message"]["content"]
                        carb.log_warn(f"Successful response, length: {len(response_text)}")
                        return response_text
                    else:
                        error_msg = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
                        carb.log_error(f"API error: {error_msg}")
                        return error_msg

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            carb.log_error(f"Exception during LLM query: {error_msg}")
            return error_msg
        
    def get_system_prompt(self) -> str:
        """Get basic system prompt for scene analysis"""
        return self._get_language_specific_system_prompt("English")

    def set_provider(self, provider: str):
        """Set current LLM provider"""
        if provider in self.providers:
            self.current_provider = provider
            carb.log_warn(f"LLM provider set to: {provider}")
            print(f"LLM provider set to: {provider}")
        else:
            print(f"Unknown provider: {provider}")

    def set_api_key(self, provider: str, api_key: str):
        """Store API key for a provider"""
        if provider in self.providers:
            setting_path = self.providers[provider]["api_key_setting"]
            self.settings.set_string(setting_path, api_key)
            print(f"API key stored for {provider}")

    # def toggle_rag(self, enable: bool):
    #     """Enable or disable RAG functionality"""
    #     self.use_rag = True
        # if self.use_rag:
        #     success = self.rag_manager.initialize_rag()
        #     if success:
        #         print("RAG functionality enabled")
        #         carb.log_warn("RAG functionality enabled")
        #     else:
        #         print("Failed to enable RAG functionality")
        #         carb.log_error("Failed to enable RAG functionality")
        #         self.use_rag = False
        # else:
        #     print("RAG functionality disabled")
        #     carb.log_warn("RAG functionality disabled")

    

    # async def query(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
    #     """Send query to current LLM provider or RAG system if enabled"""
    #     carb.log_warn(f"Query started with provider: {self.current_provider}, RAG enabled: {self.use_rag}")
    #     # If RAG is enabled and this is a user query, try RAG first
    #     if self.use_rag and len(messages) > 1 and messages[-1]["role"] == "user":
    #         user_query = messages[-1]["content"]
    #         carb.log_warn(f"Attempting RAG query with: '{user_query[:50]}...'")
    #         try:
    #             rag_response = await self.rag_manager.query_rag(user_query)
    #             carb.log_warn(f"RAG response received: {rag_response}, length: {len(rag_response) if rag_response else 0}")

    #             if rag_response and not rag_response.startswith("Error:"):
    #                 # Append RAG context to the system message or create a new one
    #                 has_system = any(msg["role"] == "system" for msg in messages)
    #                 if has_system:
    #                     for i, msg in enumerate(messages):
    #                         if msg["role"] == "system":
    #                             carb.log_warn("Adding RAG context to existing system message")
    #                             messages[i]["content"] += "\n\nAdditional context from documents:\n" + rag_response
    #                             break
    #                 else:
    #                     carb.log_warn("Creating new system message with RAG context")
    #                     messages.insert(0, {
    #                         "role": "system",
    #                         "content": "Additional context from documents:\n" + rag_response
    #                     })
    #             else:
    #                 carb.log_warn(f"RAG returned error or empty response: {rag_response[:100] if rag_response else 'None'}")
    #         except Exception as e:
    #             carb.log_error(f"RAG query failed: {str(e)}, falling back to standard LLM query")
                
    #     # Continue with standard LLM query
    #     provider_config = self.providers[self.current_provider]
    #     api_key = self.settings.get_as_string(provider_config["api_key_setting"])

    #     if not api_key:
    #         carb.log_error(f"No API key configured for {self.current_provider}")
    #         return "Error: No API key configured for " + self.current_provider

    #     carb.log_warn(f"Preparing LLM query with model: {provider_config['model']}")
    #     headers = {
    #         "Authorization": f"Bearer {api_key}",
    #         "Content-Type": "application/json"
    #     }

    #     data = {
    #         "model": provider_config["model"],
    #         "messages": messages,
    #         "temperature": temperature
    #     }
        
    #     message_count = len(messages)
    #     token_estimate = sum(len(msg["content"].split()) * 1.3 for msg in messages)
    #     carb.log_warn(f"Sending query with {message_count} messages, approx {int(token_estimate)} tokens")

    #     try:
    #         carb.log_warn(f"Sending request to: {provider_config['url']}")
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(
    #                 provider_config["url"],
    #                 headers=headers,
    #                 json=data
    #             ) as response:
    #                 carb.log_warn(f"Response received, status: {response.status}")
    #                 result = await response.json()

    #                 if response.status == 200:
    #                     response_text = result["choices"][0]["message"]["content"]
    #                     carb.log_warn(f"Successful response, length: {len(response_text)}")
    #                     return response_text
    #                 else:
    #                     error_msg = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
    #                     carb.log_error(f"API error: {error_msg}")
    #                     return error_msg

    #     except Exception as e:
    #         error_msg = f"Error: {str(e)}"
    #         carb.log_error(f"Exception during LLM query: {error_msg}")
    #         return error_msg

    # async def query(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
    #     """Send query to current LLM provider"""
    #     provider_config = self.providers[self.current_provider]
    #     api_key = self.settings.get_as_string(provider_config["api_key_setting"])

    #     if not api_key:
    #         return "Error: No API key configured for " + self.current_provider

    #     headers = {
    #         "Authorization": f"Bearer {api_key}",
    #         "Content-Type": "application/json"
    #     }

    #     data = {
    #         "model": provider_config["model"],
    #         "messages": messages,
    #         "temperature": temperature
    #     }

    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(
    #                 provider_config["url"],
    #                 headers=headers,
    #                 json=data
    #             ) as response:
    #                 result = await response.json()

    #                 if response.status == 200:
    #                     return result["choices"][0]["message"]["content"]
    #                 else:
    #                     return f"Error: {result.get('error', {}).get('message', 'Unknown error')}"

    #     except Exception as e:
    #         return f"Error: {str(e)}"

    # def get_system_prompt(self) -> str:
    #     """Get system prompt for scene analysis"""
    #     return """You are an industrial USD scene assistant for NVIDIA Omniverse.
    #     You help users understand and analyze their 3D scenes by answering questions about:
    #     - Scene hierarchy and structure
    #     - Prim properties and attributes
    #     - Materials and shaders
    #     - Transformations and relationships
    #     - Performance optimization
    #     - Best practices for USD workflows

    #     Be technical and precise, but also explain complex concepts clearly.
    #     Use the provided scene context to give accurate, helpful answers."""
