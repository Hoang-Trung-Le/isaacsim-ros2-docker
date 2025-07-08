# API Integration Guide

This document provides comprehensive information on integrating external systems with the OmniAlert extension.

## Overview

OmniAlert supports multiple integration methods to receive and process alerts from external systems:

- **HTTP REST API**: Traditional REST endpoints for alert polling
- **WebSocket**: Real-time alert streaming
- **JSON Message Format**: Standardized alert data structure

## Quick Start

### Basic Configuration

1. **Configure API Endpoint**:
   ```json
   {
     "base_url": "http://your-api-server:8000",
     "api_key": "your-api-key-here",
     "polling_interval": 10.0
   }
   ```

2. **Enable Connection**:
   - Open OmniAlert → API tab
   - Enter your configuration
   - Click "Connect"

3. **Test Connection**:
   - Use the "Test Connection" button
   - Verify in console logs: `[APIClient] Connection successful`

## Alert Data Format

### Standard Alert Structure

All alerts must conform to this JSON structure:

```json
{
  "id": "alert-uuid-12345",
  "title": "Equipment Failure",
  "message": "Conveyor belt motor has stopped responding",
  "severity": "critical",
  "category": "equipment",
  "status": "new",
  "timestamp": 1703123456.789,
  "source": "conveyor_monitor",
  "tags": ["urgent", "production"],
  "metadata": {
    "equipment_id": "CONV_001",
    "maintenance_required": true,
    "estimated_downtime": "2 hours"
  },
  "location": {
    "x": 15.5,
    "y": 8.2,
    "z": 1.0,
    "prim_path": "/World/Warehouse/Conveyor_001",
    "camera_distance": 5.0,
    "camera_angle": {
      "pitch": -30.0,
      "yaw": 45.0,
      "roll": 0.0
    }
  },
  "affected_objects": [
    "/World/Warehouse/Conveyor_001",
    "/World/Warehouse/ProductionLine_A"
  ],
  "actions": [
    {
      "id": "inspect",
      "label": "Inspect Equipment",
      "icon": "🔍",
      "callback": "navigate_to_location",
      "parameters": {
        "zoom_level": "close"
      }
    },
    {
      "id": "maintenance",
      "label": "Schedule Maintenance",
      "icon": "🔧",
      "callback": "schedule_maintenance",
      "parameters": {
        "priority": "high",
        "estimated_duration": 120
      }
    }
  ]
}
```

### Field Descriptions

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the alert |
| `title` | string | Brief alert title |
| `message` | string | Detailed alert description |
| `severity` | string | Alert severity: "critical", "high", "medium", "low", "info" |
| `category` | string | Alert category: "safety", "equipment", "process", etc. |
| `timestamp` | number | Unix timestamp (seconds since epoch) |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Current status: "new", "acknowledged", "in_progress", "resolved", "dismissed" |
| `source` | string | System or service that generated the alert |
| `tags` | array | List of tags for categorization |
| `metadata` | object | Additional alert-specific data |
| `location` | object | 3D location information for camera navigation |
| `affected_objects` | array | List of USD prim paths affected by this alert |
| `actions` | array | Available actions for this alert |

#### Location Object

```json
{
  "x": 10.5,           // X coordinate in the scene
  "y": 5.2,            // Y coordinate in the scene
  "z": 1.8,            // Z coordinate in the scene
  "prim_path": "/World/Equipment/Device_01",  // USD prim path
  "camera_distance": 5.0,  // Camera distance from target
  "camera_angle": {        // Optional camera angles
    "pitch": -30.0,        // Vertical angle (degrees)
    "yaw": 45.0,           // Horizontal angle (degrees)
    "roll": 0.0            // Roll angle (degrees)
  }
}
```

#### Action Object

```json
{
  "id": "unique_action_id",      // Unique action identifier
  "label": "Action Label",       // Display text for the action
  "icon": "🔍",                  // Emoji or icon for the action
  "callback": "function_name",   // Function to call when executed
  "parameters": {                // Additional parameters for the action
    "key": "value"
  }
}
```

## API Endpoints

### Fetch Alerts

**Endpoint**: `GET /api/alerts`

**Query Parameters**:
- `since` (optional): Unix timestamp to fetch alerts since this time
- `limit` (optional): Maximum number of alerts to return
- `severity` (optional): Filter by severity levels (comma-separated)
- `category` (optional): Filter by categories (comma-separated)

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/alerts?since=1703123456&limit=50&severity=critical,high" \
     -H "X-API-Key: your-api-key"
```

**Example Response**:
```json
{
  "alerts": [
    {
      "id": "alert-001",
      "title": "Critical Equipment Failure",
      "message": "Pump P-101 has failed",
      "severity": "critical",
      "category": "equipment",
      "timestamp": 1703123456.789,
      "location": {
        "x": 10.0,
        "y": 5.0,
        "z": 1.5,
        "prim_path": "/World/Equipment/Pump_P101"
      }
    }
  ],
  "total": 1,
  "timestamp": 1703123500.0
}
```

### Send Alert Actions

**Endpoint**: `POST /alerts/{alert_id}/actions`

**Request Body**:
```json
{
  "action": "acknowledge",
  "user": "operator_01",
  "parameters": {
    "note": "Investigating the issue"
  },
  "timestamp": 1703123456.789
}
```

**Response**:
```json
{
  "success": true,
  "message": "Action processed successfully",
  "alert_id": "alert-001",
  "action": "acknowledge"
}
```

## WebSocket Integration

### Connection

**URL**: `ws://localhost:8000/ws`

**Headers**:
```
X-API-Key: your-api-key
```

### Message Format

#### Incoming Alert Messages

```json
{
  "type": "alert",
  "data": {
    // Standard alert object
  }
}
```

#### Alert Update Messages

```json
{
  "type": "alert_update",
  "data": {
    "alert_id": "alert-001",
    "status": "acknowledged",
    "acknowledged_by": "operator_01",
    "timestamp": 1703123456.789
  }
}
```

#### Heartbeat Messages

```json
{
  "type": "heartbeat",
  "timestamp": 1703123456.789
}
```

### Example WebSocket Client

```python
import asyncio
import websockets
import json

async def alert_client():
    uri = "ws://localhost:8000/ws"
    headers = {"X-API-Key": "your-api-key"}
    
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "alert":
                    print(f"New alert: {data['data']['title']}")
                elif data["type"] == "alert_update":
                    print(f"Alert updated: {data['data']['alert_id']}")
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break
```

## Alert Templates

### Using Predefined Templates

OmniAlert includes predefined templates for common industrial scenarios. You can reference these templates when creating alerts:

```json
{
  "template": "equipment_failure",
  "parameters": {
    "equipment_id": "PUMP_001",
    "location": "/World/Equipment/Pump_001",
    "severity": "critical"
  }
}
```

### Available Templates

- `equipment_failure`: Critical equipment malfunctions
- `safety_violation`: Safety protocol violations
- `process_anomaly`: Process parameter deviations
- `environmental_warning`: Environmental condition alerts
- `employee_safety`: Employee safety concerns
- `inventory_alert`: Inventory level warnings
- `quality_issue`: Quality control problems
- `security_breach`: Security incidents

## Integration Examples

### FastAPI Server Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import uuid

app = FastAPI()

class Alert(BaseModel):
    id: Optional[str] = None
    title: str
    message: str
    severity: str
    category: str
    timestamp: Optional[float] = None
    location: Optional[dict] = None

alerts_db = []

@app.get("/api/alerts")
async def get_alerts(
    since: Optional[float] = None,
    limit: Optional[int] = 100,
    severity: Optional[str] = None
):
    filtered_alerts = alerts_db
    
    if since:
        filtered_alerts = [a for a in filtered_alerts if a["timestamp"] > since]
    
    if severity:
        severity_list = severity.split(",")
        filtered_alerts = [a for a in filtered_alerts if a["severity"] in severity_list]
    
    return {
        "alerts": filtered_alerts[:limit],
        "total": len(filtered_alerts),
        "timestamp": time.time()
    }

@app.post("/alerts")
async def create_alert(alert: Alert):
    alert_dict = alert.dict()
    alert_dict["id"] = alert_dict["id"] or str(uuid.uuid4())
    alert_dict["timestamp"] = alert_dict["timestamp"] or time.time()
    
    alerts_db.append(alert_dict)
    return {"success": True, "alert_id": alert_dict["id"]}
```

### Node.js WebSocket Server Example

```javascript
const WebSocket = require('ws');
const express = require('express');

const app = express();
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

const alerts = [];

// WebSocket connection handler
wss.on('connection', (ws, req) => {
    console.log('Client connected');
    
    // Send existing alerts
    alerts.forEach(alert => {
        ws.send(JSON.stringify({
            type: 'alert',
            data: alert
        }));
    });
    
    // Handle client messages
    ws.on('message', (message) => {
        const data = JSON.parse(message);
        console.log('Received:', data);
    });
    
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

// Function to broadcast new alert
function broadcastAlert(alert) {
    const message = JSON.stringify({
        type: 'alert',
        data: alert
    });
    
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
}

server.listen(8000, () => {
    console.log('Server running on port 8000');
});
```

## Error Handling

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Unauthorized | Check API key |
| 404 | Endpoint not found | Verify API endpoint URL |
| 422 | Invalid alert data | Check alert format |
| 500 | Server error | Check server logs |
| 1006 | WebSocket closed abnormally | Check network connection |

### Retry Logic

OmniAlert implements automatic retry logic for failed requests:

- **HTTP Requests**: 3 retry attempts with exponential backoff
- **WebSocket**: Automatic reconnection with increasing delay
- **Connection Failures**: Manual reconnection required

### Debugging

Enable detailed logging in OmniAlert to troubleshoot integration issues:

1. Check console for `[APIClient]` messages
2. Verify alert data format with test endpoints
3. Use WebSocket debugging tools for real-time issues
4. Monitor server logs for error details

## Best Practices

### Performance

- **Batch Updates**: Send multiple alerts in a single request when possible
- **Filtering**: Use query parameters to reduce data transfer
- **Rate Limiting**: Implement rate limiting on your API server
- **Compression**: Enable gzip compression for large payloads

### Security

- **API Keys**: Use secure, rotatable API keys
- **HTTPS**: Always use HTTPS in production
- **Validation**: Validate all incoming alert data
- **Rate Limiting**: Protect against DoS attacks

### Reliability

- **Heartbeats**: Implement heartbeat mechanism for WebSocket connections
- **Error Handling**: Provide clear error messages and codes
- **Monitoring**: Monitor API performance and availability
- **Backup**: Implement backup communication channels

## Testing

### Test Alert Creation

Use this endpoint to create test alerts:

```bash
curl -X POST "http://localhost:8000/alerts" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key" \
     -d '{
       "title": "Test Alert",
       "message": "This is a test alert",
       "severity": "medium",
       "category": "system",
       "location": {
         "x": 0,
         "y": 0,
         "z": 0
       }
     }'
```

### Integration Testing

1. **Connection Testing**: Verify API connectivity
2. **Data Format Testing**: Test alert data validation
3. **WebSocket Testing**: Test real-time message delivery
4. **Error Handling Testing**: Test error scenarios
5. **Performance Testing**: Test with high alert volumes

## Support

For integration support:

1. **Documentation**: Review this guide and the main README
2. **Console Logs**: Check OmniAlert console output for detailed error messages
3. **Test Endpoints**: Use provided test endpoints to verify integration
4. **Example Code**: Reference the provided integration examples 