# Employee Management Extension - API Integration Examples

This document provides examples of how to integrate the Employee Management extension with various backend APIs, particularly FastAPI-based systems and AgentIQ-compatible services.

## FastAPI Backend Integration

### Basic FastAPI Server Setup

```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

app = FastAPI(title="Employee Management API")

class EmployeeData(BaseModel):
    employee_id: str
    position: List[float]
    timestamp: float
    ppe_data: Dict[str, Any] = {}

class WorkforceOptimizationRequest(BaseModel):
    employees: List[Dict[str, Any]]
    optimization_goals: List[str]
    constraints: Dict[str, Any]

@app.post("/agents/workforce/optimize")
async def optimize_workforce(request: WorkforceOptimizationRequest):
    # Your workforce optimization logic here
    return {
        "status": "success",
        "optimizations": [
            {
                "employee_id": "emp_001",
                "recommended_task": "warehouse_zone_a",
                "efficiency_gain": 15.2
            }
        ]
    }

@app.post("/agents/safety/analyze")
async def analyze_safety(safety_data: Dict[str, Any]):
    # Safety analysis logic
    return {
        "status": "success",
        "safety_score": 85.6,
        "violations": [],
        "recommendations": ["Ensure PPE compliance in zone A"]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # Process real-time data
        await websocket.send_json({"status": "received", "data": data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### AgentIQ-Compatible Patterns

```python
# AgentIQ-style agent configuration
AGENT_CONFIG = {
    "workforce_optimizer": {
        "type": "optimizer",
        "capabilities": ["scheduling", "allocation", "efficiency"],
        "model": "nvidia/llama-3.1-70b-instruct",
        "max_tokens": 2048,
        "temperature": 0.3
    },
    "safety_analyzer": {
        "type": "analyzer",
        "capabilities": ["ppe_detection", "compliance", "risk_assessment"],
        "model": "nvidia/neva-22b",
        "confidence_threshold": 0.8
    }
}

# AgentIQ workflow configuration
WORKFLOW_CONFIG = {
    "real_time_monitoring": {
        "triggers": ["employee_position_update", "ppe_detection"],
        "agents": ["safety_analyzer", "performance_tracker"],
        "output_format": "json",
        "priority": "high"
    }
}
```

## Isaac Sim Integration Examples

### Motion Capture Data Processing

```python
# Example of processing camera data for motion capture
def process_camera_data(camera_data):
    """
    Process camera data from real-world tracking system
    
    Expected format:
    {
        "camera_id": "cam_001",
        "timestamp": 1623456789.123,
        "detections": [
            {
                "employee_id": "emp_001",
                "bbox": {"x": 320, "y": 240, "width": 80, "height": 160},
                "confidence": 0.95,
                "ppe": {
                    "hard_hat": {"detected": True, "confidence": 0.89},
                    "safety_vest": {"detected": True, "confidence": 0.92}
                }
            }
        ]
    }
    """
    for detection in camera_data["detections"]:
        employee_id = detection["employee_id"]
        bbox = detection["bbox"]
        ppe_data = detection.get("ppe", {})
        
        # Update motion capture
        motion_capture_manager.update_employee_position(
            employee_id, 
            camera_data["camera_id"], 
            bbox
        )
        
        # Check safety compliance
        position = transform_bbox_to_position(bbox, camera_data["camera_id"])
        safety_manager.check_employee_safety(employee_id, position, ppe_data)
```

### USD Scene Setup

```python
# Example USD scene setup for warehouse
def setup_warehouse_scene():
    stage = omni.usd.get_context().get_stage()
    
    # Create warehouse structure
    warehouse_prim = UsdGeom.Xform.Define(stage, "/World/Warehouse")
    
    # Add safety zones
    safety_zones = [
        {"name": "ForkliftArea", "bounds": [(-20, -10, 0), (-10, 10, 3)]},
        {"name": "ChemicalStorage", "bounds": [(-5, 15, 0), (5, 25, 3)]},
        {"name": "LoadingDock", "bounds": [(-30, -5, 0), (-20, 5, 4)]}
    ]
    
    for zone in safety_zones:
        zone_prim = UsdGeom.Cube.Define(stage, f"/World/SafetyZones/{zone['name']}")
        # Set zone properties
```

## Configuration Examples

### Extension Settings

```toml
[settings]
# API Configuration
api.base_url = "http://localhost:8000"
api.websocket_url = "ws://localhost:8000/ws"
api.timeout = 30
api.retry_attempts = 3

# Motion Capture Settings
motion_capture.update_rate = 10  # FPS
motion_capture.coordinate_system = "right_handed"
motion_capture.avatar_scale = 1.0

# Analytics Settings
analytics.update_interval = 1.0  # seconds
analytics.history_length = 1000  # data points
analytics.export_format = "json"

# Safety Settings
safety.check_interval = 0.5  # seconds
safety.alert_threshold = "medium"
safety.auto_resolve_timeout = 300  # seconds
```

### Camera Calibration

```json
{
    "cameras": {
        "cam_001": {
            "location": "warehouse_entrance",
            "world_origin": [0, -20, 3],
            "field_of_view": {"horizontal": 80, "vertical": 60},
            "resolution": {"width": 1920, "height": 1080},
            "calibration": {
                "scale_x": 0.01,
                "scale_y": 0.01,
                "offset_x": 960,
                "offset_y": 540,
                "rotation": 0
            }
        },
        "cam_002": {
            "location": "warehouse_center",
            "world_origin": [0, 0, 5],
            "field_of_view": {"horizontal": 90, "vertical": 70},
            "resolution": {"width": 1920, "height": 1080},
            "calibration": {
                "scale_x": 0.008,
                "scale_y": 0.008,
                "offset_x": 960,
                "offset_y": 540,
                "rotation": 0
            }
        }
    }
}
```

## Usage Examples

### Adding Employees Programmatically

```python
# Add multiple employees with initial positions
employees = [
    {"id": "emp_001", "position": [0, 0, 0], "role": "forklift_operator"},
    {"id": "emp_002", "position": [5, 5, 0], "role": "warehouse_worker"},
    {"id": "emp_003", "position": [-5, 10, 0], "role": "supervisor"}
]

for emp in employees:
    motion_capture_manager.add_employee(emp["id"], emp["position"])
```

### Real-time Data Streaming

```python
import asyncio
import websockets
import json

async def stream_employee_data():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            # Get current employee data
            employee_data = motion_capture_manager.get_tracking_status()
            
            # Send to backend
            await websocket.send(json.dumps({
                "type": "employee_update",
                "timestamp": time.time(),
                "data": employee_data
            }))
            
            # Receive analysis results
            response = await websocket.recv()
            analysis = json.loads(response)
            
            # Apply analysis results
            if analysis.get("safety_alerts"):
                for alert in analysis["safety_alerts"]:
                    safety_manager.handle_external_alert(alert)
            
            await asyncio.sleep(0.1)  # 10 FPS
```

### Custom AI Agent Integration

```python
async def call_custom_optimization_agent():
    """Example of calling a custom optimization agent"""
    
    # Gather current state
    employee_data = motion_capture_manager.get_tracking_status()["employees"]
    analytics_data = analytics_manager.calculate_kpis()
    safety_data = safety_manager.get_safety_dashboard_data()
    
    # Prepare agent payload
    payload = {
        "current_state": {
            "employees": employee_data,
            "performance": analytics_data,
            "safety": safety_data
        },
        "optimization_goals": [
            "maximize_productivity",
            "minimize_safety_risks",
            "optimize_resource_allocation"
        ],
        "constraints": {
            "max_shift_hours": 8,
            "safety_compliance_required": True,
            "available_equipment": ["forklift_001", "forklift_002"]
        }
    }
    
    # Call AI agent
    result = await ai_agent_manager.call_agent("workforce_optimizer", payload)
    
    if result:
        # Apply recommendations
        recommendations = result.get("recommendations", [])
        for rec in recommendations:
            apply_workforce_recommendation(rec)
```

## Troubleshooting

### Common Issues

1. **Connection Issues**: Check API endpoint configuration and network connectivity
2. **Coordinate Transformation**: Verify camera calibration parameters
3. **Performance**: Adjust update rates for better performance
4. **Safety Alerts**: Check PPE detection confidence thresholds

### Debugging

```python
# Enable debug logging
carb.settings.get_settings().set_bool("/persistent/exts/omni.employee_management/debug_mode", True)

# Check system status
status = {
    "ai_agents": ai_agent_manager.get_agent_status(),
    "motion_capture": motion_capture_manager.get_tracking_status(),
    "analytics": analytics_manager.get_analytics_status(),
    "safety": safety_manager.get_monitoring_status()
}
print(json.dumps(status, indent=2))
```
