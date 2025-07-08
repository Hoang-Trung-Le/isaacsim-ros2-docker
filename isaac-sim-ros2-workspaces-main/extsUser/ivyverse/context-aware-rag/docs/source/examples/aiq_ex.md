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

## AIQ

This example demonstrates how to use NVIDIA's Context-Aware RAG (CA-RAG) system with AIQ for document processing and question answering. The example shows how to:
- Ingest documents using AIQ
- Perform question answering using AIQ

### Prerequisites

1. NVIDIA API Keys:
   - Get your API key from: [build.nvidia.com](https://build.nvidia.com)
   - Export the following environment variable:
     ```bash
     export NVIDIA_API_KEY=your_api_key
     ```

2. Install AIQ and Context-Aware RAG:
   - Follow the installation instructions in the [AIQ Plugin Guide](../guides/aiq/aiq_install.md)
   - Make sure you have both AIQ and Context-Aware RAG installed in your environment

3. Set up pre-requisites containers:
    - [Docker Deployment](../guides/docker/compose.md)

### Setup

1. Start the AIQ services:
   - Start Ingestion Service:
     ```bash
     aiq serve --config_file=./src/vss_ctx_rag/aiq_config/workflow/config-ingestion-workflow.yml --port 8000
     ```
   - Start Retrieval Service:
     ```bash
     aiq serve --config_file=./src/vss_ctx_rag/aiq_config/workflow/config-retrieval-workflow.yml --port 8001
     ```

### Usage

1. **Document Ingestion**:
   - Documents are processed and uploaded to the AIQ ingestion service
   - The system maintains document order

2. **Question Answering**:
   - Send questions to the AIQ retrieval service
   - Receive answers based on the ingested document content

### Example Notebook

The [qna_aiq.ipynb](https://github.com/NVIDIA/context-aware-rag/blob/main/examples/qna_aiq.ipynb) notebook provides a step-by-step walkthrough of the entire process, including:
- Service initialization
- Document processing and ingestion
- Question answering examples

### Notes

- Make sure to stop the AIQ services when you're done by pressing `Ctrl+C` in the terminal windows
