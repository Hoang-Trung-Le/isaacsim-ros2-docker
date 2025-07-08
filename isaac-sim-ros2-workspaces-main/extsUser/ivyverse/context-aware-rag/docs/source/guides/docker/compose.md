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

# Docker Compose

## Running the Service with Docker Compose

### Prerequisites

-   [Docker](https://docs.docker.com/)
-   [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

#### Setting up env

Create a .env file in the root directory and set the following
variables:

``` bash
NVIDIA_API_KEY=<IF USING NVIDIA> #NVIDIA API key
NVIDIA_VISIBLE_DEVICES=<GPU ID> #GPU ID, e.g. 0

OPENAI_API_KEY=<IF USING OPENAI> #OpenAI API key

VSS_CTX_PORT_RET=<DATA RETRIEVAL PORT> #data retrieval port, e.g. 8000
VSS_CTX_PORT_IN=<DATA INGESTION PORT> #data ingestion port, e.g. 8001
```

### Using docker compose

#### First build the containers

``` bash
make -C docker build
```

#### Start the services

``` bash
make -C docker start_compose
```

This will start the following services:

-   ctx-rag-data-ingestion
-   ctx-rag-data-retrieval
-   neo4j
    -   UI available at <http://>\<HOST\>:7474
-   milvus
-   otel-collector
-   jaeger
    -   UI available at <http://>\<HOST\>:16686
-   prometheus
    -   UI available at <http://>\<HOST\>:9090
-   cassandra

To change the storage volumes, export DOCKER_VOLUME_DIRECTORY to the
desired directory.

#### Stop the services

``` bash
make -C docker stop_compose
```
