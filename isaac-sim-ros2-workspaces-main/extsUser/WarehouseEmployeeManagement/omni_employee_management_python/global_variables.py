EXTENSION_TITLE = "omni.employee_management"
EXTENSION_DESCRIPTION = (
    "Professional Employee Management System for Smart Warehouse/Factory"
)

# API Configuration
# Use localhost since AgentIQ will run in the same container
DEFAULT_API_BASE_URL = "http://localhost:1234"
DEFAULT_WEBSOCKET_URL = "ws://localhost:1234/ws"

# Docker environment detection
import os

DOCKER_ENV = os.getenv("DOCKER_ENV", "false").lower() == "true"
if DOCKER_ENV:
    # In Docker, services communicate via localhost
    DEFAULT_API_BASE_URL = "http://localhost:1234"

# Module Configuration
MOTION_CAPTURE_ENABLED = True
ANALYTICS_ENABLED = True
SAFETY_MONITORING_ENABLED = True

# Update Intervals (in seconds)
MOTION_UPDATE_INTERVAL = 0.1  # 10 FPS for smooth motion
ANALYTICS_UPDATE_INTERVAL = 1.0  # 1 second for analytics
SAFETY_CHECK_INTERVAL = 0.5  # 2 FPS for safety monitoring

# Avatar Configuration
DEFAULT_AVATAR_SCALE = 1.0
DEFAULT_AVATAR_COLOR = (0.2, 0.6, 1.0)  # Blue
SAFETY_VIOLATION_COLOR = (1.0, 0.2, 0.2)  # Red

# Coordinate System
COORDINATE_SYSTEM = "RIGHT_HANDED"  # Isaac Sim standard
