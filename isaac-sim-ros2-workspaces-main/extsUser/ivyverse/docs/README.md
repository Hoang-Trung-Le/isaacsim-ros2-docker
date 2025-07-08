# Usage

To enable this extension, run Isaac Sim with the flags --ext-folder {path_to_ext_folder} --enable {ext_directory_name}

# Ivyverse RAG Integration

This extension integrates NVIDIA's Context-Aware RAG (Retrieval Augmented Generation) system with the Ivyverse extension for Isaac Sim.

## Prerequisites

1. Install Docker and Docker Compose
2. Clone the Context-Aware RAG repository: `git clone https://github.com/NVIDIA/context-aware-rag.git`
3. Make sure the RAG services are running using the provided script: `./scripts/start_rag_services.sh`

## Usage

1. Enable RAG in the Ivyverse UI by checking the "Enable RAG" checkbox
2. Ingest documents by providing a path to a text file and clicking "Ingest"
3. Ask questions in the chat interface - the system will automatically use RAG to provide context-aware answers

## Configuration

The RAG system is configured to use the default settings with:
- Ingestion service on port 8085
- Retrieval service on port 8086 
- Default UUID "1"

To modify these settings, edit the `rag_manager.py` file.