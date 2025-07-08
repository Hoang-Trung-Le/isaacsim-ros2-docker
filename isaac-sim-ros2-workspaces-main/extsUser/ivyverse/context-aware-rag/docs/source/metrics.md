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

# Metrics

## Otel and TimeMeasure Metrics

The codebase uses OpenTelemetry for tracing and metrics. The following
environment variables can be set to enable metrics:

``` bash
export VIA_CTX_RAG_ENABLE_OTEL=true
export VIA_CTX_RAG_EXPORTER=otlp # or console
export VIA_CTX_RAG_OTEL_ENDPOINT=http://otel_collector:4318 # only used if VIA_CTX_RAG_EXPORTER is otlp
```

Traces capture TimeMeasure metrics which are used to monitor the execution time of the different components.

#### Example Span

```json
{
  "name": "GraphRetrieval/Neo4jRetriever",
  "context": {
    "trace_id": "0x0ddaa0e6800dd0f4172746f53a3fc12b",
    "span_id": "0xbf4c3dc3c9050e0e",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-04-09T05:37:28.633505Z",
  "end_time": "2025-04-09T05:37:28.752445Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "span name": "GraphRetrieval/Neo4jRetriever",
    "execution_time_ms": 119.0345287322998
  },
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "service.name": "vss-ctx-rag-default"
    },
    "schema_url": ""
  }
}
```

#### Important TimeMeasure Metrics

##### Context Manager
-   `context_manager/reset`: Time taken to reset the context manager
-   `context_manager/call`: Time taken to call the context manager
-   `context_manager/add_doc`: Time taken to add a document to the context manager
-   `context_manager/aprocess_doc`: Time taken to process a document in the context manager

##### Document Processing
-   `Add Doc`: Time taken to add a document to the document processing
-   `milvusdb/add caption`: Time taken to add a caption to the milvus database
-   `Milvus/AddSummries`: Time taken to add summaries to the milvus database

##### Graph RAG
###### Graph Extraction
-   `GraphRAG/aprocess-doc`: Time taken to process a document in the graph extraction
-   `GraphRAG/aprocess-doc/graph-create`: Time taken to create a graph in the graph extraction
-   `GraphRAG/aprocess-doc/graph-create/create-relation`: Time taken to create a relation in the graph extraction
-   `GraphRAG/aprocess-doc/graph-create/combine-chunks`: Time taken to combine chunks in the graph extraction
-   `GraphRAG/aprocess-doc/graph-create/postprocessing`: Time taken to postprocess the graph in the graph extraction
-   `GraphRAG/aprocess-doc/graph-create/convert`: Time taken to convert the graph in the graph extraction
-   `GraphRAG/aprocess-doc/create-fulltext`: Time taken to create a fulltext in the graph extraction
-   `GraphExtraction/UpdateKNN`: Time taken to update the KNN in the graph extraction
-   `GraphExtraction/VectorIndex`: Time taken to create a vector index in the graph extraction
-   `GraphExtraction/FetchEntEmbd`: Time taken to fetch the entity embedding in the graph extraction
-   `GraphExtraction/UpdatEmbding`: Time taken to update the embedding in the graph extraction

###### Graph Retrieval
-   `GraphRetrieval/Neo4jRetriever`: Time taken to retrieve the graph in the graph retrieval
-   `GraphRetrieval/CreateDocRetChain`: Time taken to create a document retrieval chain in the graph retrieval
-   `GraphRetrieval/HumanMessage`: Time taken to create a human message in the graph retrieval
-   `GraphRetrieval/AIMsg`: Time taken to create a AI message in the graph retrieval
-   `GraphRetrieval/SummarizeChat`: Time taken to summarize the chat in the graph retrieval
-   `Retrive documents`: Time taken to retrieve the documents in the graph retrieval
-   `Retrieve documents with filter`: Time taken to retrieve the documents with filter in the graph retrieval
-   `chat/process documents`: Time taken to process the documents in the chat

##### Vector RAG
-   `VectorRAG/aprocess-doc/metrics_dump`: Time taken to dump the metrics in the vector RAG
-   `VectorRAG/retrieval`: Time taken to retrieve the documents in the vector RAG

##### Summarization
-   `OffBatchSumm/Acall`: Time taken to call the summarization in the summarization
-   `summ/acall/batch-aggregation-summary`: Time taken to aggregate the summary in the summarization
-   `OffBatSumm/AggPipeline`: Time taken to aggregate the pipeline in the summarization
-   `OffBatSumm/BaseCase`: Time taken to create a base case in the summarization
-   `summ/aprocess_doc`: Time taken to asynchronously process the document in the summarization

##### Notification
-   `notifier/llm_call`: Time taken to call the LLM in the notification
-   `notifier/notify_call`: Time taken to notify the user in the notification
