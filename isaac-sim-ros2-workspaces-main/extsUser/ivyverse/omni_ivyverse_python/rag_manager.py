import os
import requests
import json
import carb
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List


class RAGManager:
    """Manages Context-Aware RAG integration for Ivyverse"""

    def __init__(self):
        self.settings = carb.settings.get_settings()
        self.rag_initialized = False
        # self.host_ip = "172.17.0.1"  # This is typically the Docker host IP from inside a container
        self.host_ip = (
            "localhost"  # This is for deploying extension directly on local machine
        )
        # Default configuration - you might want to make these configurable
        self.ingestion_url = f"http://{self.host_ip}:8087/init"
        self.retrieval_url = f"http://{self.host_ip}:8086/init"
        self.call_url = f"http://{self.host_ip}:8086/call"
        self.uuid = "1"  # Default UUID used in the RAG service
        self.config_path = (
            "/app/config/config.yaml"  # Default config path in Docker container
        )

    def initialize_rag(self) -> bool:
        """Initialize the RAG service"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {"config_path": self.config_path, "uuid": self.uuid}

            # Initialize retrieval service
            response = requests.post(self.retrieval_url, headers=headers, json=data)
            if response.status_code != 200:
                carb.log_error(
                    f"Failed to initialize RAG retrieval service: {response.text}"
                )
                return False

            carb.log_info("RAG retrieval service initialized successfully")
            self.rag_initialized = True
            return True

        except Exception as e:
            carb.log_error(f"Error initializing RAG service: {str(e)}")
            return False

    def ingest_document(self, file_path: str) -> bool:
        """Ingest a document into the RAG system"""
        if not os.path.exists(file_path):
            carb.log_error(f"File not found: {file_path}")
            return False

        try:
            # First ensure RAG is initialized
            if not self.rag_initialized:
                if not self.initialize_rag():
                    return False

            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    doc_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    doc_content = f.read()

            # Add document URL needs to be fixed - it should use 'add_doc' endpoint
            # The port should match the ingestion service (8085 or 8087)
            add_doc_url = f"http://{self.host_ip}:8087/add_doc"  # Adjust port if needed

            headers = {"Content-Type": "application/json"}
            add_doc_data = {
                "document": doc_content,
                "doc_index": 0,
                "doc_metadata": {
                    "streamId": f"doc-{os.path.basename(file_path)}",
                    "chunkIdx": 0,
                    "file": os.path.basename(file_path),
                    "is_first": True,
                    "is_last": True,  # Mark as last document to trigger processing
                    "uuid": self.uuid,
                },
            }

            response = requests.post(add_doc_url, headers=headers, json=add_doc_data)
            if response.status_code != 200:
                carb.log_error(f"Failed to ingest document: {response.text}")
                return False

            carb.log_info(
                f"Document ingested successfully: {os.path.basename(file_path)}"
            )
            return True

        except Exception as e:
            carb.log_error(f"Error ingesting document: {str(e)}")
            return False

    async def query_rag(
        self, question: str, language: str = "English"
    ) -> Optional[str]:
        """Query the RAG system with a question, with language context"""
        carb.log_warn(
            f"Starting RAG query for question: '{question[:50]}...' in {language}"
        )
        if not self.rag_initialized:
            carb.log_warn("RAG service not initialized. Attempting to initialize now.")
            if not self.initialize_rag():
                return "Error: Failed to initialize RAG service."

        # Add language context to the question for better RAG responses
        enhanced_question = question
        if language == "Japanese":
            enhanced_question = f"Please provide context for this question in a way that supports Japanese language responses: {question}"

        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "state": {"chat": {"question": enhanced_question, "is_live": False}}
            }

            # Use aiohttp instead of requests for async operation
            carb.log_info(f"Sending RAG query to {self.call_url}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.call_url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=20),  # 100-second timeout
                ) as response:
                    carb.log_info(
                        f"RAG response received with status: {response.status}"
                    )
                    if response.status != 200:
                        error_text = await response.text()
                        return f"Error: Failed to query RAG service: {error_text}"
                    result = await response.json()
                    return result["result"]

        except asyncio.TimeoutError:
            carb.log_error("RAG query timed out after 20 seconds")
            return "Error: RAG query timed out. The service may be overloaded."
        except Exception as e:
            carb.log_error(f"Error querying RAG: {str(e)}")
            return f"Error: {str(e)}"
