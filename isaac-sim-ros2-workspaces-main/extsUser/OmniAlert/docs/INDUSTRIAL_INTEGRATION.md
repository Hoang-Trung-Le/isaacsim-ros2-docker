# OmniAlert Industrial Alert Agent Integration

This document describes the integration between OmniAlert and the Industrial Alert Agent, enabling real-time alert monitoring and automatic camera navigation in Isaac Sim.

## Overview

The OmniAlert extension has been enhanced to automatically fetch alerts from the Industrial Alert Agent running on `localhost:1234` and display them as push notifications in Isaac Sim. When users click on notifications, the camera automatically navigates to the origin of the alert in the 3D scene.

## Key Features

### 🔄 Real-time Alert Monitoring
- Automatic polling of the Industrial Alert Agent every 5 seconds
- Real-time conversion of industrial alerts to OmniAlert format
- Duplicate detection to avoid showing the same alert multiple times

### 🗺️ Origin-to-Prim Mapping
- Automatic mapping of alert origins to USD prim paths
- Support for workers, equipment, zones, and production lines
- Configurable mapping dictionary for easy customization

### 🔔 Smart Notifications
- Priority-based notifications (Critical and High severity alerts)
- Click-to-navigate functionality
- Automatic acknowledgment in both systems

### 📱 Two-way Communication
- Acknowledge alerts in OmniAlert and sync to Industrial Agent
- Resolve alerts and update status across systems
- Real-time status synchronization

## Architecture

```
Industrial Alert Agent (localhost:1234)
           ↓ HTTP/WebSocket
    OmniAlert API Client
           ↓
     Alert Manager
           ↓
   Notification System → Camera Controller
           ↓                    ↓
    Push Notifications    3D Navigation
```

## Configuration

### Origin to Prim Path Mapping

The system uses a configurable mapping to translate alert origins to USD prim paths:

```python
ORIGIN_TO_PRIM_PATH = {
    "Worker_1": "/World/Worker",
    "Worker_2": "/World/Worker_2", 
    "Worker_3": "/World/Worker_3",
    "Conveyor_1": "/World/Warehouse/Conveyor_001",
    "Conveyor_2": "/World/Warehouse/Conveyor_002",
    "Equipment_1": "/World/Equipment/Device_01",
    "Equipment_2": "/World/Equipment/Device_02",
    "Pump_P101": "/World/Equipment/Pump_P101",
    "Zone_A": "/World/Warehouse/Zone_A",
    "Zone_B": "/World/Warehouse/Zone_B",
    "Zone_C": "/World/Warehouse/Zone_C",
    "ProductionLine_A": "/World/Warehouse/ProductionLine_A",
    "ProductionLine_B": "/World/Warehouse/ProductionLine_B",
}
```

### Alert Conversion

Industrial Agent alerts are automatically converted to OmniAlert format:

| Industrial Agent | OmniAlert |
|------------------|-----------|
| `severity: "high"` | `AlertSeverity.HIGH` |
| `category: "safety"` | `AlertCategory.SAFETY` |
| `status: "active"` | `AlertStatus.NEW` |
| `origin: "Worker_1"` | `location.prim_path: "/World/Worker"` |

## Usage

### 1. Start Industrial Alert Agent

Ensure the Industrial Alert Agent is running on `localhost:1234`:

```bash
# Example API endpoint that should be available
curl http://localhost:1234/industrial_alert/alerts
```

### 2. Enable OmniAlert Extension

1. Open Isaac Sim
2. Go to `Window` → `Extensions`
3. Enable "OmniAlert - Industrial Alert System"
4. The extension will automatically connect to the Industrial Agent

### 3. Monitor Alerts

1. The OmniAlert window will open automatically
2. Alerts from the Industrial Agent will appear in real-time
3. High and Critical alerts will show as push notifications
4. Click notifications to navigate to alert origins

### 4. Interact with Alerts

- **Click Notification**: Navigate to alert location and acknowledge
- **Dashboard Tab**: View all alerts and statistics
- **Industrial Agent Tab**: Monitor connection status and manual controls
- **Test Tab**: Test notifications and camera navigation

## API Endpoints

### Industrial Alert Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/industrial_alert/health` | GET | Health check |
| `/industrial_alert/alerts` | GET | Fetch all alerts |
| `/industrial_alert/alerts/{id}/acknowledge` | POST | Acknowledge alert |
| `/industrial_alert/alerts/{id}/resolve` | POST | Resolve alert |

### Example Alert Response

```json
{
  "status": "success",
  "alerts": [
    {
      "id": "IND-0001",
      "title": "Worker not wearing safety helmet",
      "description": "Computer vision system detected worker without helmet in Zone A",
      "severity": "high",
      "category": "safety",
      "location": "Zone A",
      "origin": "Worker_1",
      "status": "active",
      "source": "cv_system",
      "facility": "Industrial Facility",
      "created_at": "2025-06-20T13:57:16.357908",
      "escalated": true,
      "assigned_to": "Safety Officer"
    }
  ],
  "alert_count": 1,
  "facility_status": "CAUTION"
}
```

## Workflow Example

### Safety Alert Scenario

1. **Alert Generation**: Computer vision system detects worker without helmet
2. **Industrial Agent**: Creates alert with origin "Worker_1"
3. **OmniAlert Fetch**: Polls and retrieves new alert
4. **Conversion**: Maps "Worker_1" to "/World/Worker" prim path
5. **Notification**: Shows high-severity notification popup
6. **User Interaction**: User clicks notification
7. **Navigation**: Camera smoothly moves to worker location
8. **Acknowledgment**: Alert marked as acknowledged in both systems

## Testing

Run the integration test script:

```bash
cd extsUser/OmniAlert
python test_integration.py
```

This will test:
- Connection to Industrial Alert Agent
- Alert conversion and mapping
- Origin-to-prim path translation
- API communication

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Industrial Alert Agent
**Solutions**:
- Verify Industrial Agent is running on localhost:1234
- Check firewall settings
- Review console logs for connection errors

**Problem**: No alerts appearing
**Solutions**:
- Check Industrial Agent has alerts available
- Verify polling is enabled (Industrial Agent tab)
- Check alert severity filters

### Navigation Issues

**Problem**: Camera doesn't navigate to alert location
**Solutions**:
- Verify prim path exists in USD scene
- Check origin mapping in `ORIGIN_TO_PRIM_PATH`
- Ensure viewport is active

### Performance Issues

**Problem**: High CPU usage or lag
**Solutions**:
- Increase polling interval (default: 5 seconds)
- Reduce number of active notifications
- Clear resolved alerts regularly

## Customization

### Adding New Origins

To add support for new alert origins:

1. Update `ORIGIN_TO_PRIM_PATH` in `api_client.py`:
```python
ORIGIN_TO_PRIM_PATH["New_Equipment"] = "/World/Equipment/New_Device"
```

2. Ensure the USD prim exists in your scene

### Modifying Notification Behavior

To change which alerts trigger notifications:

1. Edit `_on_alert_added()` in `window.py`:
```python
# Show notifications for all alerts
if alert.severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH, AlertSeverity.MEDIUM]:
    self.notification_manager.notification_system.show_notification(alert)
```

### Custom Alert Actions

Add custom actions to alerts by modifying `_convert_industrial_alert_to_omni()`:

```python
alert.actions.append(
    AlertAction(
        id="custom_action",
        label="Custom Action",
        icon="🔧",
        callback="custom_callback"
    )
)
```

## Future Enhancements

- **WebSocket Support**: Real-time alerts via WebSocket connection
- **Alert Filtering**: Advanced filtering by category, severity, location
- **Historical Analytics**: Alert trend analysis and reporting
- **Multi-Agent Support**: Connect to multiple Industrial Alert Agents
- **Custom Visualizations**: 3D alert indicators in the scene
- **Voice Notifications**: Audio alerts for critical situations

## Support

For issues or questions:
1. Check console logs in Isaac Sim
2. Verify Industrial Alert Agent is responding
3. Test with the provided integration script
4. Review this documentation for troubleshooting steps 