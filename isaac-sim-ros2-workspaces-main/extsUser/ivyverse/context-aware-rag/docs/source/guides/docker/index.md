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
# Docker Deployment

This section contains guides for running and managing the VIA CTX RAG system using Docker.

## Available Guides

- [Docker Compose](compose.md) - Instructions for running the complete system using Docker Compose
- [Standalone Docker Service](docker.md) - Instructions for running individual services (Neo4j, Milvus) using Docker

## Overview

The VIA CTX RAG system uses Docker to containerize its components, making it easy to deploy and manage the following services:

- Neo4j: Graph database for storing and querying relationships
- Milvus: Vector database for similarity search
- Data Ingestion Service: For processing and storing data
- Data Retrieval Service: For querying and retrieving information

Choose the appropriate guide based on your deployment needs:
- Use the Standalone Docker guide if you want to run services individually
- Use the Docker Compose guide for a complete system deployment

```{toctree}
:hidden:
:maxdepth: 2

Docker Compose <./compose.md>
Standalone Docker <./docker.md>

```
