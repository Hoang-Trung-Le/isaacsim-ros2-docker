# import requests
# from dotenv import load_dotenv

# load_dotenv()

# #TODO: Start the nv-ingest client to process the pdf documents
# #TODO: Add Chunks to DB

# UUID = "1"

# # Initialize Data Ingestion Service

# config_path = "/app/config/config.yaml"

# url = "http://localhost:8087/init"
# headers = {
#     "Content-Type": "application/json"
# }
# data = {
#     "config_path": config_path,
#     "uuid": UUID
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)


# # Data Ingestion Service
# url = "http://localhost:8087/add_doc"
# headers = {"Content-Type": "application/json"}
# data = {
#     "document": "Omniverse Warehouse Scene Description",
#     "doc_index": 0,
#     "doc_metadata": {
#         "streamId": "doc-01",
#         "chunkIdx": 0,
#         "file": "/home/ubuntu/context-aware-rag/data/OmniverseWarehouseSceneDescription.md",
#         "is_first": True,
#         "is_last": False,
#         "uuid": UUID
#     }
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)

import requests
import argparse
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Ingest document into Context-Aware RAG")
parser.add_argument("--input", required=True, help="Path to the input document")
args = parser.parse_args()

# Validate file exists
if not os.path.exists(args.input):
    print(f"Error: File {args.input} does not exist")
    exit(1)


UUID = "1"

# Initialize Data Ingestion Service
ingestion_host = os.getenv("INGESTION_HOST", "localhost")
ingestion_port = os.getenv("INGESTION_PORT", "8087")
ingestion_url = f"http://{ingestion_host}:{ingestion_port}"

# Initialize the context manager
init_url = f"{ingestion_url}/init"
headers = {"Content-Type": "application/json"}
init_data = {
    "config_path": "/app/config/config.yaml",
    "uuid": UUID
}

response = requests.post(init_url, headers=headers, json=init_data)
print(response.text)

# Add the document
add_doc_url = f"{ingestion_url}/add_doc"

add_doc_data = {
    "document": "Omniverse Warehouse Scene Description document content",
    "doc_index": 0,
    "doc_metadata": {
        "streamId": "stream1",
        "chunkIdx": 0,
        "file": args.input,
        "is_first": True,
        "is_last": False,
        "uuid": UUID
    }
}

response = requests.post(add_doc_url, headers=headers, json=add_doc_data)
print(response.text)
