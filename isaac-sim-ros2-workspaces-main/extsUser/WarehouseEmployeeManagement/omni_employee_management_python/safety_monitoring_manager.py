import carb
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from .global_variables import SAFETY_CHECK_INTERVAL


class SafetyMonitoringManager:
    """
    Real-time safety compliance monitoring and alerting system
    Monitors PPE compliance, hazard zones, and safety protocols
    """

    def __init__(self):
        self.settings = carb.settings.get_settings()
        self.monitoring_active = False
        
        # Safety zones and rules
        self.safety_zones = {}  # zone_id -> zone configuration
        self.hazard_zones = {}  # zone_id -> hazard configuration
        self.ppe_requirements = {}  # zone_id -> required PPE list
        
        # Employee safety status
        self.employee_safety_status = defaultdict(dict)
        self.safety_violations = deque(maxlen=500)  # Keep last 500 violations
        self.compliance_history = defaultdict(lambda: deque(maxlen=100))
        
        # Alert system
        self.active_alerts = {}
        self.alert_callbacks = []
        
        # Safety metrics
        self.safety_metrics = {
            "total_checks": 0,
            "violations_detected": 0,
            "ppe_violations": 0,
            "zone_violations": 0,
            "resolved_violations": 0
        }
        
        # PPE detection confidence thresholds
        self.ppe_confidence_thresholds = {
            "hard_hat": 0.8,
            "safety_vest": 0.75,
            "safety_glasses": 0.7,
            "gloves": 0.7,
            "safety_shoes": 0.75
        }

    def initialize_safety_monitoring(self) -> bool:
        """Initialize the safety monitoring system"""
        try:
            self.monitoring_active = True
            self._setup_default_safety_zones()
            carb.log_info("Safety Monitoring: System initialized")
            return True
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Failed to initialize: {str(e)}")
            return False

    def _setup_default_safety_zones(self):
        """Setup default safety zones for warehouse/factory"""
        try:
            # Define common safety zones
            default_zones = {
                "forklift_area": {
                    "bounds": {"min": (-20, -10, 0), "max": (-10, 10, 3)},
                    "type": "hazard",
                    "risk_level": "high",
                    "required_ppe": ["hard_hat", "safety_vest", "safety_shoes"],
                    "max_personnel": 2,
                    "speed_limit": 5.0  # km/h
                },
                "heavy_machinery": {
                    "bounds": {"min": (10, -15, 0), "max": (25, 15, 5)},
                    "type": "restricted",
                    "risk_level": "high",
                    "required_ppe": ["hard_hat", "safety_vest", "safety_glasses", "safety_shoes"],
                    "authorized_personnel_only": True
                },
                "chemical_storage": {
                    "bounds": {"min": (-5, 15, 0), "max": (5, 25, 3)},
                    "type": "hazard",
                    "risk_level": "critical",
                    "required_ppe": ["hard_hat", "safety_vest", "safety_glasses", "gloves"],
                    "gas_detection_required": True
                },
                "loading_dock": {
                    "bounds": {"min": (-30, -5, 0), "max": (-20, 5, 4)},
                    "type": "active_work",
                    "risk_level": "medium",
                    "required_ppe": ["hard_hat", "safety_vest"],
                    "vehicle_interaction": True
                },
                "general_warehouse": {
                    "bounds": {"min": (-10, -10, 0), "max": (10, 10, 3)},
                    "type": "general",
                    "risk_level": "low",
                    "required_ppe": ["safety_vest"],
                    "default_zone": True
                }
            }
            
            for zone_id, config in default_zones.items():
                self.add_safety_zone(zone_id, config)
                
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Failed to setup default zones: {str(e)}")

    def add_safety_zone(self, zone_id: str, zone_config: Dict[str, Any]) -> bool:
        """Add a new safety zone"""
        try:
            required_fields = ["bounds", "type", "risk_level"]
            for field in required_fields:
                if field not in zone_config:
                    carb.log_error(f"Safety Monitoring: Missing required field {field} in zone config")
                    return False

            self.safety_zones[zone_id] = zone_config
            
            # Setup PPE requirements for this zone
            if "required_ppe" in zone_config:
                self.ppe_requirements[zone_id] = zone_config["required_ppe"]
            
            carb.log_info(f"Safety Monitoring: Added safety zone {zone_id}")
            return True
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Failed to add safety zone: {str(e)}")
            return False

    def check_employee_safety(self, employee_id: str, position: Tuple[float, float, float], 
                            ppe_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive safety check for an employee
        
        Args:
            employee_id: Employee identifier
            position: Current employee position
            ppe_data: PPE detection data with format:
                {
                    "hard_hat": {"detected": True, "confidence": 0.95},
                    "safety_vest": {"detected": True, "confidence": 0.88},
                    ...
                }
        """
        try:
            self.safety_metrics["total_checks"] += 1
            
            # Determine current zone
            current_zone = self._get_zone_from_position(position)
            
            # Initialize safety status
            safety_status = {
                "employee_id": employee_id,
                "timestamp": time.time(),
                "position": position,
                "current_zone": current_zone,
                "compliance_status": "compliant",
                "violations": [],
                "alerts": []
            }
            
            if current_zone:
                # Check zone access authorization
                zone_violations = self._check_zone_access(employee_id, current_zone, position)
                if zone_violations:
                    safety_status["violations"].extend(zone_violations)
                
                # Check PPE compliance
                if ppe_data:
                    ppe_violations = self._check_ppe_compliance(employee_id, current_zone, ppe_data)
                    if ppe_violations:
                        safety_status["violations"].extend(ppe_violations)
                
                # Check additional safety rules
                additional_violations = self._check_additional_safety_rules(employee_id, current_zone, position)
                if additional_violations:
                    safety_status["violations"].extend(additional_violations)
            
            # Update compliance status
            if safety_status["violations"]:
                safety_status["compliance_status"] = "violation"
                self.safety_metrics["violations_detected"] += 1
                
                # Record violation
                self._record_safety_violation(employee_id, safety_status)
                
                # Generate alerts
                alerts = self._generate_safety_alerts(safety_status)
                safety_status["alerts"] = alerts
            
            # Update employee safety status
            self.employee_safety_status[employee_id] = safety_status
            
            # Update compliance history
            self.compliance_history[employee_id].append({
                "timestamp": safety_status["timestamp"],
                "compliant": safety_status["compliance_status"] == "compliant",
                "zone": current_zone,
                "violation_count": len(safety_status["violations"])
            })
            
            return safety_status
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Failed to check employee safety: {str(e)}")
            return {"compliance_status": "error", "violations": [], "alerts": []}

    def _get_zone_from_position(self, position: Tuple[float, float, float]) -> Optional[str]:
        """Determine which safety zone contains the given position"""
        try:
            x, y, z = position
            
            for zone_id, zone_config in self.safety_zones.items():
                bounds = zone_config["bounds"]
                min_bounds = bounds["min"]
                max_bounds = bounds["max"]
                
                if (min_bounds[0] <= x <= max_bounds[0] and
                    min_bounds[1] <= y <= max_bounds[1] and
                    min_bounds[2] <= z <= max_bounds[2]):
                    return zone_id
            
            # Return default zone if no specific zone found
            for zone_id, zone_config in self.safety_zones.items():
                if zone_config.get("default_zone", False):
                    return zone_id
            
            return None
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error determining zone: {str(e)}")
            return None

    def _check_zone_access(self, employee_id: str, zone_id: str, position: Tuple[float, float, float]) -> List[Dict[str, Any]]:
        """Check if employee is authorized to be in the zone"""
        violations = []
        
        try:
            zone_config = self.safety_zones.get(zone_id, {})
            
            # Check authorized personnel restriction
            if zone_config.get("authorized_personnel_only", False):
                # In a real implementation, you'd check against an authorization database
                # For now, we'll simulate this check
                if not self._is_employee_authorized(employee_id, zone_id):
                    violations.append({
                        "type": "unauthorized_access",
                        "severity": "high",
                        "zone": zone_id,
                        "description": f"Unauthorized access to restricted zone: {zone_id}",
                        "position": position
                    })
                    self.safety_metrics["zone_violations"] += 1
            
            # Check maximum personnel limit
            max_personnel = zone_config.get("max_personnel")
            if max_personnel:
                current_occupancy = self._get_zone_occupancy(zone_id)
                if current_occupancy > max_personnel:
                    violations.append({
                        "type": "zone_overcrowding",
                        "severity": "medium",
                        "zone": zone_id,
                        "description": f"Zone occupancy ({current_occupancy}) exceeds limit ({max_personnel})",
                        "current_occupancy": current_occupancy,
                        "max_occupancy": max_personnel
                    })
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error checking zone access: {str(e)}")
        
        return violations

    def _check_ppe_compliance(self, employee_id: str, zone_id: str, ppe_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check PPE compliance for the current zone"""
        violations = []
        
        try:
            required_ppe = self.ppe_requirements.get(zone_id, [])
            
            for ppe_item in required_ppe:
                ppe_status = ppe_data.get(ppe_item, {})
                detected = ppe_status.get("detected", False)
                confidence = ppe_status.get("confidence", 0.0)
                
                threshold = self.ppe_confidence_thresholds.get(ppe_item, 0.7)
                
                if not detected or confidence < threshold:
                    violations.append({
                        "type": "ppe_violation",
                        "severity": "high",
                        "zone": zone_id,
                        "ppe_item": ppe_item,
                        "detected": detected,
                        "confidence": confidence,
                        "threshold": threshold,
                        "description": f"Missing or undetected PPE: {ppe_item} in zone {zone_id}"
                    })
                    self.safety_metrics["ppe_violations"] += 1
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error checking PPE compliance: {str(e)}")
        
        return violations

    def _check_additional_safety_rules(self, employee_id: str, zone_id: str, position: Tuple[float, float, float]) -> List[Dict[str, Any]]:
        """Check additional safety rules specific to the zone"""
        violations = []
        
        try:
            zone_config = self.safety_zones.get(zone_id, {})
            
            # Check for gas detection requirement
            if zone_config.get("gas_detection_required", False):
                # In a real implementation, you'd check gas sensor data
                # For simulation, we'll randomly trigger this occasionally
                import random
                if random.random() < 0.01:  # 1% chance of gas detection alert
                    violations.append({
                        "type": "gas_detection_alert",
                        "severity": "critical",
                        "zone": zone_id,
                        "description": "Gas detection alert in chemical storage area",
                        "action_required": "Immediate evacuation"
                    })
            
            # Check vehicle interaction zones
            if zone_config.get("vehicle_interaction", False):
                # Check for proper safety protocols around vehicles
                # This would integrate with vehicle tracking systems
                pass
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error checking additional rules: {str(e)}")
        
        return violations

    def _record_safety_violation(self, employee_id: str, safety_status: Dict[str, Any]):
        """Record a safety violation for tracking and reporting"""
        try:
            violation_record = {
                "employee_id": employee_id,
                "timestamp": safety_status["timestamp"],
                "zone": safety_status["current_zone"],
                "violations": safety_status["violations"],
                "position": safety_status["position"]
            }
            
            self.safety_violations.append(violation_record)
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error recording violation: {str(e)}")

    def _generate_safety_alerts(self, safety_status: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts based on safety violations"""
        alerts = []
        
        try:
            for violation in safety_status["violations"]:
                alert = {
                    "alert_id": f"{safety_status['employee_id']}_{int(safety_status['timestamp'])}",
                    "type": "safety_violation",
                    "severity": violation.get("severity", "medium"),
                    "employee_id": safety_status["employee_id"],
                    "violation_type": violation["type"],
                    "description": violation["description"],
                    "zone": safety_status["current_zone"],
                    "timestamp": safety_status["timestamp"],
                    "status": "active"
                }
                
                alerts.append(alert)
                self.active_alerts[alert["alert_id"]] = alert
                
                # Trigger alert callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        carb.log_error(f"Safety Monitoring: Alert callback error: {str(e)}")
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error generating alerts: {str(e)}")
        
        return alerts

    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        try:
            if alert_id in self.active_alerts:
                self.active_alerts[alert_id]["status"] = "resolved"
                self.active_alerts[alert_id]["resolved_timestamp"] = time.time()
                self.safety_metrics["resolved_violations"] += 1
                carb.log_info(f"Safety Monitoring: Alert {alert_id} resolved")
                return True
            else:
                carb.log_warn(f"Safety Monitoring: Alert {alert_id} not found")
                return False
                
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error resolving alert: {str(e)}")
            return False

    def get_safety_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive safety dashboard data"""
        try:
            current_time = time.time()
            
            # Calculate compliance rates
            total_employees = len(self.employee_safety_status)
            compliant_employees = sum(
                1 for status in self.employee_safety_status.values()
                if status["compliance_status"] == "compliant"
            )
            compliance_rate = (compliant_employees / total_employees * 100) if total_employees > 0 else 100
            
            # Get active violations
            active_violations = [
                status for status in self.employee_safety_status.values()
                if status["compliance_status"] == "violation"
            ]
            
            # Get recent violations (last hour)
            recent_violations = [
                v for v in self.safety_violations
                if current_time - v["timestamp"] <= 3600
            ]
            
            dashboard_data = {
                "overview": {
                    "total_employees": total_employees,
                    "compliant_employees": compliant_employees,
                    "compliance_rate": compliance_rate,
                    "active_violations": len(active_violations),
                    "active_alerts": len([a for a in self.active_alerts.values() if a["status"] == "active"])
                },
                "metrics": self.safety_metrics,
                "active_violations": active_violations,
                "recent_violations": recent_violations,
                "zone_status": self._get_zone_status(),
                "alert_summary": self._get_alert_summary()
            }
            
            return dashboard_data
            
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error getting dashboard data: {str(e)}")
            return {}

    def _get_zone_status(self) -> Dict[str, Any]:
        """Get status of all safety zones"""
        zone_status = {}
        
        try:
            for zone_id, zone_config in self.safety_zones.items():
                occupancy = self._get_zone_occupancy(zone_id)
                max_occupancy = zone_config.get("max_personnel", "unlimited")
                
                zone_violations = [
                    status for status in self.employee_safety_status.values()
                    if status["current_zone"] == zone_id and status["compliance_status"] == "violation"
                ]
                
                zone_status[zone_id] = {
                    "type": zone_config["type"],
                    "risk_level": zone_config["risk_level"],
                    "current_occupancy": occupancy,
                    "max_occupancy": max_occupancy,
                    "violations": len(zone_violations),
                    "status": "safe" if len(zone_violations) == 0 else "alert"
                }
                
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error getting zone status: {str(e)}")
        
        return zone_status

    def _get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of alerts by type and severity"""
        alert_summary = {
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_type": defaultdict(int),
            "total_active": 0,
            "total_resolved": 0
        }
        
        try:
            for alert in self.active_alerts.values():
                if alert["status"] == "active":
                    alert_summary["total_active"] += 1
                    severity = alert.get("severity", "medium")
                    alert_summary["by_severity"][severity] += 1
                    alert_summary["by_type"][alert["violation_type"]] += 1
                else:
                    alert_summary["total_resolved"] += 1
                    
        except Exception as e:
            carb.log_error(f"Safety Monitoring: Error getting alert summary: {str(e)}")
        
        return alert_summary

    def _get_zone_occupancy(self, zone_id: str) -> int:
        """Get current number of people in a zone"""
        return sum(
            1 for status in self.employee_safety_status.values()
            if status["current_zone"] == zone_id
        )

    def _is_employee_authorized(self, employee_id: str, zone_id: str) -> bool:
        """Check if employee is authorized for restricted zone (placeholder)"""
        # In a real implementation, this would check against an authorization database
        # For simulation, we'll assume some employees are authorized
        return employee_id.endswith(("1", "2", "3"))  # Simple simulation

    def add_alert_callback(self, callback: callable):
        """Add a callback function to be called when alerts are generated"""
        self.alert_callbacks.append(callback)

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring system status"""
        return {
            "active": self.monitoring_active,
            "zones_configured": len(self.safety_zones),
            "employees_monitored": len(self.employee_safety_status),
            "total_violations": len(self.safety_violations),
            "active_alerts": len([a for a in self.active_alerts.values() if a["status"] == "active"]),
            "metrics": self.safety_metrics
        }
