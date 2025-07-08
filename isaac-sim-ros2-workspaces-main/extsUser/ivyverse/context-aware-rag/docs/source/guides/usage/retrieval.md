<!--
SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
 *
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 *
http://www.apache.org/licenses/LICENSE-2.0
 *
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Retrieval

This guide explains how to query documents in the Context-Aware RAG system.

## Making Queries

Queries can be made to the system using the `/call` endpoint of the Retrieval Service.

### Request Format

```json
{
  "state": {
    "chat": {
      "question": "Your question here",
      "is_live": false,
    }
  }
}
```

### Example Query

```python
import requests

url = "http://localhost:8000/call"
headers = {"Content-Type": "application/json"}
data = {
    "state": {
        "chat": {
            "question": "What topics are covered in the document?",
            "is_live": False,
        }
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

### Query Parameters

- `question`: The actual question you want to ask about the documents
- `is_live`: Set to `true` for real-time queries, `false` for batch processing

## Best Practices

1. **Question Formulation**
   - Be specific and clear in your questions
   - Use natural language
   - Avoid overly complex or multi-part questions

2. **Query Timing**
   - For real-time applications, set `is_live: true`
   - For batch processing, set `is_live: false`

3. **Error Handling**
   - Always check response status codes
   - Handle timeouts appropriately
   - Implement retry logic for failed requests
