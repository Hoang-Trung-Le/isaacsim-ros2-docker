import carb
import aiohttp
import json
from typing import Dict, Any, Optional, List
class LLMManager:
    """Manages LLM providers and API calls"""
    
    def __init__(self):
        self.settings = carb.settings.get_settings()
        self.current_provider = "NVIDIA NIM"
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
    
    def set_provider(self, provider: str):
        """Set current LLM provider"""
        if provider in self.providers:
            self.current_provider = provider
            print(f"LLM provider set to: {provider}")
        else:
            print(f"Unknown provider: {provider}")
    
    def set_api_key(self, provider: str, api_key: str):
        """Store API key for a provider"""
        if provider in self.providers:
            setting_path = self.providers[provider]["api_key_setting"]
            self.settings.set_string(setting_path, api_key)
            print(f"API key stored for {provider}")
    
    async def query(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
        """Send query to current LLM provider"""
        provider_config = self.providers[self.current_provider]
        api_key = self.settings.get_as_string(provider_config["api_key_setting"])
        
        if not api_key:
            return "Error: No API key configured for " + self.current_provider
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": provider_config["model"],
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    provider_config["url"],
                    headers=headers,
                    json=data
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200:
                        return result["choices"][0]["message"]["content"]
                    else:
                        return f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_system_prompt(self) -> str:
        """Get system prompt for scene analysis"""
        return """You are an industrial USD scene assistant for NVIDIA Omniverse. 
        You help users understand and analyze their 3D scenes by answering questions about:
        - Scene hierarchy and structure
        - Prim properties and attributes
        - Materials and shaders
        - Transformations and relationships
        - Performance optimization
        - Best practices for USD workflows
        
        Be technical and precise, but also explain complex concepts clearly.
        Use the provided scene context to give accurate, helpful answers."""
