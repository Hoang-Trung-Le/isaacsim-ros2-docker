# OmniAlert - Ivygilant - Industrial Alert System

A comprehensive real-time alert and notification system for warehouse and factory digital twins built for NVIDIA Omniverse Isaac Sim.

## Overview

OmniAlert provides real-time push notifications and a unified alert dashboard for operational errors, warnings, and critical alerts in industrial environments. The extension features color-coded notifications by severity, camera navigation to affected locations, and seamless integration with FastAPI AgentIQ endpoints.

## Features

### Core Functionality
- **Real-time Alert Processing**: Fetch and display alerts from external APIs with WebSocket and polling support
- **Color-coded Severity System**: Visual indicators for Critical, High, Medium, Low, and Info alerts
- **3D Scene Navigation**: Click-to-zoom camera functionality for affected locations in the 3D scene
- **Professional Industrial UI**: Clean, modern interface designed for engineers and managers
- **Central Dashboard**: Unified alert management with filtering, search, and acknowledgment capabilities

### Alert Management
- **Alert Lifecycle**: Complete workflow from creation to resolution
- **Status Tracking**: New → Acknowledged → In Progress → Resolved/Dismissed
- **Bulk Operations**: Acknowledge all, resolve all, clear resolved alerts
- **Search & Filtering**: Filter by severity, category, status, and text search
- **Export Capabilities**: Export alerts to JSON or CSV formats

### Notification System
- **Popup Notifications**: Non-intrusive notifications with auto-dismiss
- **Sound Alerts**: Audio notifications for critical alerts (configurable)
- **Notification Queue**: Manage multiple alerts with priority-based display
- **Emergency Controls**: Emergency stop to dismiss all notifications

### Integration
- **FastAPI Integration**: Connect to external alert systems and AgentIQ workflows
- **WebSocket Support**: Real-time alert streaming
- **HTTP Polling**: Fallback polling mechanism
- **Authentication**: API key support for secure connections

## Installation

1. Copy the extension to your Omniverse `exts` or `extsUser` folder:
   ```
   extsUser/OmniAlert/
   ```

2. Enable the extension in the Extension Manager:
   - Open Window → Extensions
   - Search for "OmniAlert"
   - Enable the extension

3. The OmniAlert window will appear in the Window menu: `Window → OmniAlert Dashboard`

## Configuration

### API Configuration
Configure your alert data sources in the API tab:

```json
{
  "base_url": "http://localhost:8000",
  "websocket_url": "ws://localhost:8000/ws",
  "api_key": "your-api-key",
  "polling_interval": 10.0
}
```

### Notification Settings
Customize notification behavior:

```json
{
  "notification_timeout": 5.0,
  "max_notifications": 5,
  "enable_sound": true,
  "severity_filters": {
    "critical": true,
    "high": true,
    "medium": true,
    "low": false,
    "info": false
  }
}
```

## Usage

### Basic Operation

1. **Starting the System**:
   - Open the OmniAlert window from `Window → OmniAlert Dashboard`
   - Configure API connection in the API tab
   - Click "Connect" to start receiving alerts

2. **Managing Alerts**:
   - View active alerts in the Dashboard tab
   - Click alert items to navigate to affected locations
   - Use acknowledge/resolve buttons for alert lifecycle management
   - Apply filters to focus on specific alert types

3. **Emergency Procedures**:
   - Use the Emergency Stop button to dismiss all notifications
   - Critical alerts will automatically trigger visual and audio notifications

### Advanced Features

#### Custom Alert Templates
Create custom alert templates using the provided JSON structure:

```json
{
  "title": "Custom Alert",
  "severity": "high",
  "category": "equipment",
  "message_template": "Alert for {device_id} in {location}",
  "actions": [
    {
      "id": "inspect",
      "label": "Inspect Device",
      "icon": "🔍",
      "callback": "navigate_to_location"
    }
  ]
}
```

#### Camera Navigation
Alerts with location data enable automatic camera navigation:
- Click the "🔍 View" button on any alert
- Camera smoothly animates to the alert location
- Configurable animation duration and camera distance

#### Bulk Operations
Manage multiple alerts efficiently:
- **Acknowledge All New**: Mark all new alerts as acknowledged
- **Resolve All Acknowledged**: Resolve all acknowledged alerts
- **Clear Resolved**: Remove resolved alerts from the dashboard
- **Export**: Save alert data for analysis

## API Integration

### Alert Data Format
Alerts must follow the standard format:

```json
{
  "id": "unique-alert-id",
  "title": "Alert Title",
  "message": "Detailed alert message",
  "severity": "critical",
  "category": "safety",
  "status": "new",
  "timestamp": 1703123456.789,
  "location": {
    "x": 10.5,
    "y": 5.2,
    "z": 1.8,
    "prim_path": "/World/Equipment/Device_01"
  },
  "source": "safety_monitor",
  "tags": ["urgent", "equipment"],
  "affected_objects": ["/World/Equipment/Device_01"]
}
```

### Supported Endpoints
- `GET /api/alerts` - Fetch alerts
- `POST /alerts/{id}/actions` - Send alert actions
- `WebSocket /ws` - Real-time alert streaming

## Architecture

### Components
- **AlertManager**: Core alert state management
- **NotificationSystem**: Popup and sound notifications
- **CameraController**: 3D scene navigation
- **APIClient**: External system integration
- **AlertDashboard**: Main UI dashboard

### Data Flow
1. **Alert Ingestion**: API client fetches alerts from external sources
2. **Processing**: Alert manager processes and stores alerts
3. **Notification**: Notification system displays popups for new alerts
4. **Interaction**: Users interact with alerts through the dashboard
5. **Actions**: Alert actions are sent back to external systems

## Troubleshooting

### Common Issues

**Connection Problems**:
- Verify API endpoint URLs and network connectivity
- Check API key authentication
- Review console logs for detailed error messages

**Missing Notifications**:
- Check notification filters in settings
- Verify alert severity levels
- Ensure sound is enabled for audio alerts

**Camera Navigation Issues**:
- Verify alert location data is provided
- Check that referenced prims exist in the scene
- Adjust camera animation settings if needed

### Logging
The extension provides detailed logging. Check the console for:
- `[AlertManager]` - Alert processing messages
- `[APIClient]` - API connection and data transfer
- `[CameraController]` - Camera navigation events
- `[NotificationSystem]` - Notification display events

## Support

For issues, feature requests, or integration support:
- Check the troubleshooting section above
- Review console logs for error details
- Consult the API integration documentation

## License

This extension is part of the Omniverse Isaac Sim ecosystem. Please refer to the NVIDIA Omniverse license terms for usage guidelines. 