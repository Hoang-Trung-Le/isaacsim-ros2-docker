"""
Comprehensive Alert Types for OmniAlert Extension
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import time
import uuid


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    
    @property
    def level(self) -> str:
        return self.value
    
    @property
    def priority(self) -> int:
        """Return priority level for sorting (higher = more urgent)"""
        priority_map = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "info": 1
        }
        return priority_map.get(self.value, 0)


class AlertCategory(Enum):
    """Alert category types"""
    SAFETY = "safety"
    EQUIPMENT = "equipment"
    PRODUCTION = "production"
    PROCESS = "process"
    ENVIRONMENTAL = "environmental"
    EMPLOYEE = "employee"
    INVENTORY = "inventory"
    QUALITY = "quality"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"
    
    @property
    def display_name(self) -> str:
        return self.value.title()


class AlertStatus(Enum):
    """Alert status types"""
    NEW = "new"
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


@dataclass
class AlertLocation:
    """Alert location information"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    prim_path: Optional[str] = None
    camera_distance: float = 5.0
    camera_angle: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        if self.camera_angle is None:
            self.camera_angle = {"pitch": -30.0, "yaw": 45.0, "roll": 0.0}


@dataclass
class AlertAction:
    """Alert action definition"""
    id: str
    label: str
    icon: str
    callback: str
    parameters: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


@dataclass
class Alert:
    """Comprehensive alert data structure"""
    
    id: str
    title: str
    message: str
    severity: AlertSeverity
    category: AlertCategory
    status: AlertStatus = AlertStatus.NEW
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    location: Optional[AlertLocation] = None
    affected_objects: List[str] = field(default_factory=list)
    actions: List[AlertAction] = field(default_factory=list)
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[float] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[float] = None
    
    # Legacy fields for backward compatibility
    description: str = ""
    origin: str = ""
    created_at: str = ""
    
    def __post_init__(self):
        # Handle legacy fields and conversions
        if not self.message and self.description:
            self.message = self.description
        
        if not self.created_at:
            self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        
        # Convert string severity to enum if needed
        if isinstance(self.severity, str):
            try:
                self.severity = AlertSeverity(self.severity.lower())
            except ValueError:
                self.severity = AlertSeverity.MEDIUM
        
        # Convert string category to enum if needed
        if isinstance(self.category, str):
            try:
                self.category = AlertCategory(self.category.lower())
            except ValueError:
                self.category = AlertCategory.SYSTEM
        
        # Convert string status to enum if needed
        if isinstance(self.status, str):
            try:
                self.status = AlertStatus(self.status.lower())
            except ValueError:
                self.status = AlertStatus.NEW
    
    @classmethod
    def from_industrial_data(cls, data: Dict[str, Any]) -> "Alert":
        """Create alert from industrial agent data"""
        
        # Parse location information
        location = None
        if "location" in data or "origin" in data:
            # Try to get location from origin mapping
            from .api_client import ORIGIN_TO_PRIM_PATH
            origin = data.get("origin", "")
            prim_path = ORIGIN_TO_PRIM_PATH.get(origin)
            
            if prim_path:
                location = AlertLocation(
                    x=data.get("x", 0.0),
                    y=data.get("y", 0.0),
                    z=data.get("z", 0.0),
                    prim_path=prim_path
                )
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", "Industrial Alert"),
            message=data.get("description", data.get("message", "")),
            severity=data.get("severity", "medium"),
            category=data.get("category", "system"),
            status=data.get("status", "new"),
            timestamp=time.time(),
            source="industrial_agent",
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            location=location,
            affected_objects=data.get("affected_objects", []),
            # Legacy fields
            description=data.get("description", ""),
            origin=data.get("origin", ""),
            created_at=data.get("created_at", ""),
        )
    
    def acknowledge(self, user: str) -> None:
        """Acknowledge the alert"""
        self.status = AlertStatus.ACKNOWLEDGED
        self.acknowledged_by = user
        self.acknowledged_at = time.time()
    
    def resolve(self, user: str) -> None:
        """Resolve the alert"""
        self.status = AlertStatus.RESOLVED
        self.resolved_by = user
        self.resolved_at = time.time()
    
    def dismiss(self, user: str) -> None:
        """Dismiss the alert"""
        self.status = AlertStatus.DISMISSED
        self.resolved_by = user
        self.resolved_at = time.time()
    
    def is_active(self) -> bool:
        """Check if alert is active (not resolved or dismissed)"""
        return self.status not in [AlertStatus.RESOLVED, AlertStatus.DISMISSED]
    
    def get_age_seconds(self) -> float:
        """Get alert age in seconds"""
        return time.time() - self.timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "source": self.source,
            "tags": self.tags,
            "metadata": self.metadata,
            "location": {
                "x": self.location.x,
                "y": self.location.y,
                "z": self.location.z,
                "prim_path": self.location.prim_path,
                "camera_distance": self.location.camera_distance,
                "camera_angle": self.location.camera_angle
            } if self.location else None,
            "affected_objects": self.affected_objects,
            "actions": [
                {
                    "id": action.id,
                    "label": action.label,
                    "icon": action.icon,
                    "callback": action.callback,
                    "parameters": action.parameters
                } for action in self.actions
            ],
            "acknowledged_by": self.acknowledged_by,
            "acknowledged_at": self.acknowledged_at,
            "resolved_by": self.resolved_by,
            "resolved_at": self.resolved_at,
        }


def create_alert_from_template(
    template_name: str,
    title: Optional[str] = None,
    message: Optional[str] = None,
    severity: Optional[AlertSeverity] = None,
    category: Optional[AlertCategory] = None,
    location: Optional[AlertLocation] = None,
    source: str = "template",
    **kwargs
) -> Alert:
    """Create an alert from a template"""
    
    # Default templates
    templates = {
        "equipment_failure": {
            "title": "Equipment Failure Detected",
            "message": "Equipment failure detected and requires immediate attention.",
            "severity": AlertSeverity.CRITICAL,
            "category": AlertCategory.EQUIPMENT,
        },
        "safety_violation": {
            "title": "Safety Violation Detected",
            "message": "Safety violation detected in operational area.",
            "severity": AlertSeverity.HIGH,
            "category": AlertCategory.SAFETY,
        },
        "process_anomaly": {
            "title": "Process Anomaly Detected",
            "message": "Process anomaly detected in operational parameters.",
            "severity": AlertSeverity.MEDIUM,
            "category": AlertCategory.PROCESS,
        },
        "environmental_warning": {
            "title": "Environmental Condition Warning",
            "message": "Environmental condition out of acceptable range.",
            "severity": AlertSeverity.MEDIUM,
            "category": AlertCategory.ENVIRONMENTAL,
        },
        "employee_safety": {
            "title": "Employee Safety Alert",
            "message": "Employee safety concern detected.",
            "severity": AlertSeverity.HIGH,
            "category": AlertCategory.EMPLOYEE,
        },
        "inventory_alert": {
            "title": "Inventory Alert",
            "message": "Inventory level alert detected.",
            "severity": AlertSeverity.LOW,
            "category": AlertCategory.INVENTORY,
        },
        "quality_issue": {
            "title": "Quality Control Issue",
            "message": "Quality control issue detected.",
            "severity": AlertSeverity.MEDIUM,
            "category": AlertCategory.QUALITY,
        },
        "security_breach": {
            "title": "Security Breach Alert",
            "message": "Security breach detected.",
            "severity": AlertSeverity.CRITICAL,
            "category": AlertCategory.SECURITY,
        },
    }
    
    # Get template or use default
    template = templates.get(template_name, templates["equipment_failure"])
    
    # Override with provided values
    alert_data = {
        "id": str(uuid.uuid4()),
        "title": title or template["title"],
        "message": message or template["message"],
        "severity": severity or template["severity"],
        "category": category or template["category"],
        "location": location,
        "source": source,
        **kwargs
    }
    
    return Alert(**alert_data)


def create_test_alert(
    severity: AlertSeverity = AlertSeverity.MEDIUM,
    category: AlertCategory = AlertCategory.SYSTEM,
    location: Optional[AlertLocation] = None
) -> Alert:
    """Create a test alert for debugging"""
    
    return Alert(
        id=f"TEST-{int(time.time())}",
        title=f"Test {severity.level.title()} Alert",
        message=f"This is a test {severity.level} alert for {category.display_name} category",
        severity=severity,
        category=category,
        location=location,
        source="test",
        tags=["test", "debug"],
        metadata={"test": True, "created_by": "test_function"}
    )
