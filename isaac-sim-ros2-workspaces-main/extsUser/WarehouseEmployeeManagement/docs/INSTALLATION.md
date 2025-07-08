# Employee Management Extension - Installation & Deployment Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

## Prerequisites

### System Requirements
- **Isaac Sim Version**: 2024.1.0 or later
- **Python Version**: 3.10+
- **Operating System**: Windows 10/11, Ubuntu 20.04+, or CentOS 7+
- **GPU**: NVIDIA RTX 3070 or better (RTX 4080+ recommended for production)
- **VRAM**: Minimum 8GB, 16GB+ recommended
- **RAM**: 32GB minimum, 64GB recommended for production

### Required Dependencies
- NVIDIA Omniverse Isaac Sim
- Python packages: `numpy`, `scipy`, `requests`, `asyncio`, `opencv-python`
- Network access for AI agent integration
- Camera hardware (IP cameras or USB cameras with OpenCV support)

## Installation Methods

### Method 1: Direct Installation (Recommended)

1. **Clone or Download Extension**
   ```bash
   # Navigate to Isaac Sim extensions directory
   cd ~/.local/share/ov/pkg/isaac_sim-*/exts
   
   # Create extension directory
   mkdir -p employee_management
   cd employee_management
   
   # Copy extension files
   cp -r /path/to/EmployeeManagement/* .
   ```

2. **Register Extension**
   - Open Isaac Sim
   - Go to `Window` → `Extensions`
   - Click the gear icon (Settings)
   - Add extension search path: `~/.local/share/ov/pkg/isaac_sim-*/exts/employee_management`
   - Refresh extension list

3. **Enable Extension**
   - Search for "Employee Management"
   - Toggle the extension to enable it
   - The extension window should appear automatically

### Method 2: Development Installation

1. **Setup Development Environment**
   ```bash
   # Create symbolic link for development
   ln -s /path/to/EmployeeManagement ~/.local/share/ov/pkg/isaac_sim-*/exts/employee_management
   ```

2. **Enable Developer Mode**
   - In Isaac Sim, go to `Help` → `About`
   - Enable "Developer Mode" if available
   - This allows hot-reloading of extension changes

### Method 3: Omniverse Hub Installation

1. **Package Extension**
   ```bash
   # Create extension package
   cd /path/to/EmployeeManagement
   zip -r employee_management_extension.zip . -x "*.git*" "*.pyc" "__pycache__/*"
   ```

2. **Install via Hub**
   - Open Omniverse Hub
   - Go to Extensions tab
   - Click "Install from file"
   - Select the ZIP package

## Configuration

### Initial Setup

1. **Launch Configuration Wizard**
   - Open Isaac Sim
   - Load your warehouse/factory scene
   - Open the Employee Management window
   - Click "Settings" → "Setup Wizard"

2. **Camera Configuration**
   ```yaml
   # Example camera configuration
   cameras:
     - name: "Camera_01"
       type: "IP"
       url: "rtsp://192.168.1.100:554/stream1"
       resolution: [1920, 1080]
       fps: 30
       
     - name: "Camera_02"
       type: "USB"
       device_id: 0
       resolution: [1280, 720]
       fps: 30
   ```

3. **AI Agent Configuration**
   ```json
   {
     "ai_agent": {
       "api_endpoint": "https://your-api-endpoint.com/v1",
       "api_key": "your-api-key-here",
       "timeout": 30,
       "retry_attempts": 3
     }
   }
   ```

### Advanced Configuration

1. **Safety Zones Setup**
   ```python
   # Define safety zones in your scene
   safety_zones = [
       {
           "id": "forklift_area",
           "type": "vehicle_operation",
           "bounds": {"x_min": 0, "x_max": 20, "y_min": 10, "y_max": 30},
           "required_ppe": ["hard_hat", "safety_vest", "steel_toes"]
       },
       {
           "id": "chemical_storage",
           "type": "hazardous_materials",
           "bounds": {"x_min": 50, "x_max": 70, "y_min": 0, "y_max": 15},
           "required_ppe": ["respirator", "chemical_gloves", "eye_protection"]
       }
   ]
   ```

2. **Performance Tuning**
   ```yaml
   performance:
     update_frequency: 30  # Hz
     max_tracked_employees: 50
     history_retention_days: 30
     analytics_computation_interval: 60  # seconds
   ```

## Verification

### Basic Functionality Test

1. **Extension Loading**
   ```python
   # Check in Isaac Sim Python console
   import omni.ext
   print(omni.ext.get_extension_manager().get_enabled_extensions())
   # Should include 'omni.employee.management.python'
   ```

2. **Camera Connection Test**
   - Open Employee Management window
   - Go to Motion Capture tab
   - Click "Test Camera Connection"
   - Verify camera feeds are displayed

3. **Coordinate Transformation Test**
   - Click on camera view to mark a point
   - Verify corresponding world coordinates are reasonable
   - Check avatar movement in Isaac Sim scene

### Advanced Testing

1. **Run Unit Tests**
   ```bash
   cd /path/to/EmployeeManagement
   python tests/test_employee_management.py
   ```

2. **Performance Benchmarking**
   ```python
   # Monitor performance metrics
   import psutil
   import time
   
   # Check CPU/memory usage while extension is running
   process = psutil.Process()
   print(f"CPU: {process.cpu_percent()}%")
   print(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
   ```

## Troubleshooting

### Common Issues

1. **Extension Not Loading**
   ```
   Problem: Extension doesn't appear in Extensions list
   Solution: 
   - Check file permissions
   - Verify extension.toml syntax
   - Check Isaac Sim logs: ~/.nvidia-omniverse/logs/Kit/Isaac-Sim/
   ```

2. **Camera Connection Failed**
   ```
   Problem: "Failed to connect to camera" error
   Solution:
   - Verify camera URL/device ID
   - Check network connectivity
   - Test camera with external tools (VLC, etc.)
   - Check firewall settings
   ```

3. **Poor Performance**
   ```
   Problem: High CPU usage or low frame rate
   Solution:
   - Reduce camera resolution
   - Lower update frequency
   - Limit number of tracked employees
   - Check GPU memory usage
   ```

4. **Coordinate Transformation Issues**
   ```
   Problem: Avatars appear in wrong positions
   Solution:
   - Recalibrate cameras
   - Verify calibration point accuracy
   - Check world coordinate system orientation
   ```

### Debug Mode

Enable debug logging:
```python
import carb
carb.settings.get_settings().set("/app/employee_management/debug", True)
```

Check logs:
```bash
# Linux/Mac
tail -f ~/.nvidia-omniverse/logs/Kit/Isaac-Sim/kit.log

# Windows
Get-Content -Path "$env:USERPROFILE\.nvidia-omniverse\logs\Kit\Isaac-Sim\kit.log" -Wait
```

## Production Deployment

### Hardware Requirements

**Recommended Production Setup:**
- **Server**: Intel Xeon or AMD EPYC processor
- **GPU**: NVIDIA RTX A6000 or RTX 6000 Ada
- **Memory**: 128GB RAM minimum
- **Storage**: NVMe SSD, 2TB+
- **Network**: Gigabit Ethernet, redundant connections

### Scalability Considerations

1. **Multi-Camera Support**
   ```yaml
   deployment:
     max_cameras: 16
     processing_threads: 8
     memory_buffer_size: "2GB"
   ```

2. **Load Balancing**
   ```python
   # Distribute processing across multiple instances
   worker_config = {
       "motion_capture_workers": 4,
       "analytics_workers": 2,
       "safety_monitoring_workers": 2
   }
   ```

3. **Data Storage**
   ```sql
   -- Example database schema for analytics
   CREATE TABLE employee_metrics (
       id SERIAL PRIMARY KEY,
       employee_id VARCHAR(50),
       timestamp TIMESTAMP,
       position_x FLOAT,
       position_y FLOAT,
       position_z FLOAT,
       productivity_score FLOAT,
       safety_compliance BOOLEAN
   );
   ```

### Monitoring and Maintenance

1. **Health Checks**
   ```python
   # Automated health monitoring
   def system_health_check():
       checks = {
           "extension_loaded": check_extension_status(),
           "cameras_connected": check_camera_connections(),
           "ai_agent_responsive": check_ai_agent_status(),
           "performance_acceptable": check_performance_metrics()
       }
       return checks
   ```

2. **Automated Backups**
   ```bash
   #!/bin/bash
   # Backup script for configuration and calibration data
   DATE=$(date +%Y%m%d_%H%M%S)
   tar -czf "employee_mgmt_backup_$DATE.tar.gz" \
       data/camera_calibration.json \
       data/safety_zones.json \
       config/
   ```

3. **Update Procedures**
   ```bash
   # Safe update procedure
   1. Stop Isaac Sim
   2. Backup current configuration
   3. Deploy new extension version
   4. Test in development mode
   5. Switch to production
   ```

### Security Considerations

1. **API Security**
   - Use HTTPS for all API communications
   - Implement API key rotation
   - Monitor API usage for anomalies

2. **Camera Security**
   - Use secure camera protocols (HTTPS/RTSP over TLS)
   - Implement camera authentication
   - Regular firmware updates

3. **Data Privacy**
   - Encrypt stored employee data
   - Implement data retention policies
   - Comply with privacy regulations (GDPR, etc.)

## Support

For technical support:
- **Documentation**: Check `/docs/` directory
- **Issues**: Report bugs via issue tracker
- **Community**: Join the Omniverse developer community
- **Enterprise Support**: Contact NVIDIA professional services

---

*Last updated: December 2024*
*Version: 1.0.0*
