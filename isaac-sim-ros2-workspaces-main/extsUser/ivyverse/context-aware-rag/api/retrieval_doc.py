# import requests
# from dotenv import load_dotenv

# load_dotenv()

# UUID = "1"

# # Initialize Data Retrieval Service

# config_path = "/app/config/config.yaml"

# url = "http://localhost:8086/init"
# headers = {
#     "Content-Type": "application/json"
# }
# data = {
#     "config_path": config_path,
#     "uuid": UUID
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)


# # Data Retrieval Service
# url = "http://localhost:8086/call"
# headers = {"Content-Type": "application/json"}
# data = {
#     "state": {
#         "chat": {
#             "question": "What topics are covered in the document?",
#             "is_live": False,
#         }
#     }
# }

# response = requests.post(url, headers=headers, json=data)
# print(f'Assistant: {response.json()["result"]}')

import requests
import argparse
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Retrieve information from Context-Aware RAG"
)
parser.add_argument(
    "--question", required=True, help="Question to ask about the document"
)
args = parser.parse_args()

UUID = "1"

# Initialize Data Retrieval Service
retrieval_host = os.getenv("RETRIEVAL_HOST", "localhost")
retrieval_port = os.getenv("RETRIEVAL_PORT", "8086")
retrieval_url = f"http://{retrieval_host}:{retrieval_port}"

# Initialize the context manager (with the same UUID as ingestion)
init_url = f"{retrieval_url}/init"
headers = {"Content-Type": "application/json"}
init_data = {
    "config_path": "/app/config/config.yaml",
    "uuid": UUID
}

response = requests.post(init_url, headers=headers, json=init_data)
print(response.text)

# Send the question
call_url = f"{retrieval_url}/call"
call_data = {"state": {"chat": {"question": args.question, "is_live": False}}}

response = requests.post(call_url, headers=headers, json=call_data)
result = response.json()
print(f'Assistant: {result.get("result", "No result returned")}')
