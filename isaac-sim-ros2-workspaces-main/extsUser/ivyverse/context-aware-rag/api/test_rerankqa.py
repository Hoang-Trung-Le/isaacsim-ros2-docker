import requests
import os

nvidia_api_key = os.environ.get("NVIDIA_API_KEY")

invoke_url = "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nv-rerankqa-1b-v2/reranking"

print(f"Invoke URL: {invoke_url}")

headers = {
    "Authorization": f"Bearer {nvidia_api_key}",
    "Accept": "application/json",
}

payload = {
  "model": "nvidia/llama-3.2-nv-rerankqa-1b-v2",
  "query": {
    "text": "What is the GPU memory bandwidth of H100 SXM?"
  },
  "passages": [
    {
      "text": "The Hopper GPU is paired with the Grace CPU using NVIDIA's ultra-fast chip-to-chip interconnect, delivering 900GB/s of bandwidth, 7X faster than PCIe Gen5. This innovative design will deliver up to 30X higher aggregate system memory bandwidth to the GPU compared to today's fastest servers and up to 10X higher performance for applications running terabytes of data."
    },
    {
      "text": "A100 provides up to 20X higher performance over the prior generation and can be partitioned into seven GPU instances to dynamically adjust to shifting demands. The A100 80GB debuts the world's fastest memory bandwidth at over 2 terabytes per second (TB/s) to run the largest models and datasets."
    },
    {
      "text": "Accelerated servers with H100 deliver the compute power—along with 3 terabytes per second (TB/s) of memory bandwidth per GPU and scalability with NVLink and NVSwitch™."
    }
  ]
}

# re-use connections
session = requests.Session()

response = session.post(invoke_url, headers=headers, json=payload)

response.raise_for_status()
response_body = response.json()
print(response_body)