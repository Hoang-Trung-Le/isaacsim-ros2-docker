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

# Optimization

## Optimization Features

-   Batch processing for efficiency:
    -   Use a custom batch processing class to process documents in
        batches
    -   Parallelizes the processing of documents
-   Separate process for context manager:
    -   Prevents context manager from blocking the main process
    -   Utilizes asynchronous processing to handle requests

## Best Practices for Performance Optimization

### Document Processing
- Batch similar documents together for efficient processing
- Use appropriate chunk sizes for optimal retrieval
- Monitor system resources during document ingestion
- Implement proper error handling and retry mechanisms

### Query Optimization
- Use appropriate batch sizes for query processing
- Implement caching for frequently accessed documents
- Monitor query latency and optimize as needed
- Use appropriate indexing strategies for your use case

### Resource Management
- Monitor system resources (CPU, memory, disk usage)
- Implement proper cleanup of temporary resources
- Use appropriate timeouts for long-running operations
- Scale services independently based on workload

### Monitoring and Metrics
- Track key performance metrics:
  - Request latency
  - Document processing time
  - Error rates
  - System resource usage
- Set up alerts for performance degradation
- Regularly review and optimize based on metrics
