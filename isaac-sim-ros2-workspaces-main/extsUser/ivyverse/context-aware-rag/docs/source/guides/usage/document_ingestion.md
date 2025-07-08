# Ingestion

This guide explains how to add documents to the Context-Aware RAG system.

## Adding Documents

Documents can be added to the system using the `/add_doc` endpoint of the Data Ingestion Service.

### Request Format

```json
{
  "document": "Your document text here",
  "doc_index": 0,
  "doc_metadata": {
    "streamId": "unique_stream_id",
    "chunkIdx": 0,
    "file": "source_file.txt",
    "is_first": true,  // Required for first document in a stream
    "is_last": false,  // Required for last document in a stream
    "uuid": "your_session_uuid"
  }
}
```

### Metadata Flags

- `is_first`: Set to `true` for the first document in a stream
- `is_last`: Set to `true` for the last document in a stream
- At least one document must have `is_first: true` and one must have `is_last: true`

### Example: Adding Multiple Documents

1. First document:
```python
import requests

url = "http://localhost:8001/add_doc"
headers = {"Content-Type": "application/json"}
data = {
    "document": "First document content",
    "doc_index": 0,
    "doc_metadata": {
        "streamId": "stream1",
        "chunkIdx": 0,
        "file": "doc.txt",
        "is_first": True,
        "is_last": False,
        "uuid": "your_session_uuid"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

2. Middle document:
```python
import requests

url = "http://localhost:8001/add_doc"
headers = {"Content-Type": "application/json"}
data = {
    "document": "Middle document content",
    "doc_index": 1,
    "doc_metadata": {
        "streamId": "stream1",
        "chunkIdx": 1,
        "file": "doc.txt",
        "uuid": "your_session_uuid"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

3. Last document:
```python
import requests

url = "http://localhost:8001/add_doc"
headers = {"Content-Type": "application/json"}
data = {
    "document": "Last document content",
    "doc_index": 2,
    "doc_metadata": {
        "streamId": "stream1",
        "chunkIdx": 2,
        "file": "doc.txt",
        "is_first": False,
        "is_last": True,
        "uuid": "your_session_uuid"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
```

## Best Practices

### Document Structure
- Keep documents between 100-1000 words for optimal retrieval
- Use clear, well-formatted text
- Include relevant metadata

### Document Indexing
- Use sequential indices starting from 0
- Maintain consistent indexing within a stream
- Include relevant metadata for better context

### Performance Optimization
- Batch similar documents together
- Use appropriate chunk sizes
- Monitor system resources
