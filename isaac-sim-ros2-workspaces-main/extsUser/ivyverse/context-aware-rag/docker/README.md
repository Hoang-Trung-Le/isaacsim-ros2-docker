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

# Running with Docker

### Prerequisites

-   Docker
-   NVIDIA Container Toolkit

#### Setting up env

Create a .env file in the root directory and set the following
variables:

``` bash
NVIDIA_API_KEY=<IF USING NVIDIA>
NVIDIA_VISIBLE_DEVICES=<GPU ID>

OPENAI_API_KEY=<IF USING OPENAI>

VSS_CTX_PORT_RET=<DATA RETRIEVAL PORT>
VSS_CTX_PORT_IN=<DATA INGESTION PORT>
```

### Using docker compose


#### Build the Context Aware RAG image

``` bash
make -C docker build
```

#### Starting the container/services

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

#### If not using docker compose - run dependent containers

#### Additional envs

``` bash
MILVUS_HOST=<HOST> #milvus host, e.g. localhost
MILVUS_PORT=<MILVUS_PORT> #milvus port, e.g. 19530

GRAPH_DB_URI=bolt://<HOST>:<NEO4J_PORT> #neo4j uri, e.g. bolt://localhost:7687
GRAPH_DB_USERNAME=<USERNAME> #neo4j username, e.g. neo4j
GRAPH_DB_PASSWORD=<PASSWORD> #neo4j password, e.g. password
```

#### neo4j

``` bash
docker run -d --name neo4j -p <PORT>:7687  neo4j:5.26.4
```

#### milvus

``` bash
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh


bash standalone_embed.sh start
```


## Build the Context Aware RAG image

Make sure you are in the project root directory.

``` bash
make -C docker build
```

## Run the data ingestion service

``` bash
make -C docker start_in
```

## Run the data retrieval service

``` bash
make -C docker start_ret
```
