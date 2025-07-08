"""
Alert Manager for OmniAlert Extension
Manages alert state and provides callbacks for alert events
"""

import carb
from typing import Dict, List, Optional, Callable, Any
from .alert_types import Alert, AlertStatus, AlertSeverity


class AlertManager:
    """Central alert management system"""

    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._callbacks: Dict[str, List[Callable]] = {
            "alert_added": [],
            "alert_updated": [],
            "alert_removed": []
        }
        carb.log_info("[AlertManager] Initialized")

    def add_alert(self, alert: Alert) -> bool:
        """Add a new alert"""
        try:
            if alert.id in self._alerts:
                carb.log_warn(f"[AlertManager] Alert {alert.id} already exists, updating")
                self.update_alert(alert)
                return True
            
            self._alerts[alert.id] = alert
            carb.log_info(f"[AlertManager] Added alert: {alert.id} - {alert.title}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_added", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to add alert: {e}")
            return False

    def update_alert(self, alert: Alert) -> bool:
        """Update an existing alert"""
        try:
            if alert.id not in self._alerts:
                carb.log_warn(f"[AlertManager] Alert {alert.id} not found, adding")
                return self.add_alert(alert)
            
            self._alerts[alert.id] = alert
            carb.log_info(f"[AlertManager] Updated alert: {alert.id}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_updated", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to update alert: {e}")
            return False

    def remove_alert(self, alert_id: str) -> bool:
        """Remove an alert"""
        try:
            if alert_id not in self._alerts:
                carb.log_warn(f"[AlertManager] Alert {alert_id} not found")
                return False
            
            alert = self._alerts.pop(alert_id)
            carb.log_info(f"[AlertManager] Removed alert: {alert_id}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_removed", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to remove alert: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[Alert]:
        """Get a specific alert by ID"""
        return self._alerts.get(alert_id)

    def get_alerts(self, 
                   active_only: bool = False,
                   severity_filter: Optional[List[AlertSeverity]] = None,
                   limit: Optional[int] = None) -> List[Alert]:
        """Get list of alerts with optional filtering"""
        alerts = list(self._alerts.values())
        
        # Filter by active status
        if active_only:
            alerts = [a for a in alerts if a.is_active()]
        
        # Filter by severity
        if severity_filter:
            alerts = [a for a in alerts if a.severity in severity_filter]
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            alerts = alerts[:limit]
        
        return alerts

    def acknowledge_alert(self, alert_id: str, user: str) -> bool:
        """Acknowledge an alert"""
        try:
            alert = self._alerts.get(alert_id)
            if not alert:
                carb.log_warn(f"[AlertManager] Alert {alert_id} not found")
                return False
            
            alert.acknowledge(user)
            carb.log_info(f"[AlertManager] Acknowledged alert: {alert_id} by {user}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_updated", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to acknowledge alert: {e}")
            return False

    def resolve_alert(self, alert_id: str, user: str) -> bool:
        """Resolve an alert"""
        try:
            alert = self._alerts.get(alert_id)
            if not alert:
                carb.log_warn(f"[AlertManager] Alert {alert_id} not found")
                return False
            
            alert.resolve(user)
            carb.log_info(f"[AlertManager] Resolved alert: {alert_id} by {user}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_updated", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to resolve alert: {e}")
            return False

    def dismiss_alert(self, alert_id: str, user: str) -> bool:
        """Dismiss an alert"""
        try:
            alert = self._alerts.get(alert_id)
            if not alert:
                carb.log_warn(f"[AlertManager] Alert {alert_id} not found")
                return False
            
            alert.dismiss(user)
            carb.log_info(f"[AlertManager] Dismissed alert: {alert_id} by {user}")
            
            # Trigger callbacks
            self._trigger_callbacks("alert_updated", alert)
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to dismiss alert: {e}")
            return False

    def clear_resolved_alerts(self) -> int:
        """Clear all resolved alerts"""
        try:
            resolved_ids = [
                alert_id for alert_id, alert in self._alerts.items()
                if alert.status in [AlertStatus.RESOLVED, AlertStatus.DISMISSED]
            ]
            
            count = 0
            for alert_id in resolved_ids:
                if self.remove_alert(alert_id):
                    count += 1
            
            carb.log_info(f"[AlertManager] Cleared {count} resolved alerts")
            return count
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to clear resolved alerts: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            alerts = list(self._alerts.values())
            
            active_alerts = [a for a in alerts if a.is_active()]
            resolved_alerts = [a for a in alerts if a.status in [AlertStatus.RESOLVED, AlertStatus.DISMISSED]]
            
            # Count by severity
            severity_counts = {}
            for severity in AlertSeverity:
                severity_counts[severity.value] = len([a for a in alerts if a.severity == severity])
            
            # Count active by severity
            active_severity_counts = {}
            for severity in AlertSeverity:
                active_severity_counts[severity.value] = len([a for a in active_alerts if a.severity == severity])
            
            return {
                "total_alerts": len(alerts),
                "active_alerts": len(active_alerts),
                "resolved_alerts": len(resolved_alerts),
                "by_severity": severity_counts,
                "active_by_severity": active_severity_counts,
            }
            
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to get statistics: {e}")
            return {
                "total_alerts": 0,
                "active_alerts": 0,
                "resolved_alerts": 0,
                "by_severity": {},
                "active_by_severity": {},
            }

    def add_callback(self, event: str, callback: Callable) -> None:
        """Add a callback for alert events"""
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
        carb.log_info(f"[AlertManager] Added callback for event: {event}")

    def remove_callback(self, event: str, callback: Callable) -> None:
        """Remove a callback for alert events"""
        if event in self._callbacks and callback in self._callbacks[event]:
            self._callbacks[event].remove(callback)
            carb.log_info(f"[AlertManager] Removed callback for event: {event}")

    def _trigger_callbacks(self, event: str, alert: Alert) -> None:
        """Trigger callbacks for an event"""
        try:
            if event in self._callbacks:
                for callback in self._callbacks[event]:
                    try:
                        callback(alert)
                    except Exception as e:
                        carb.log_error(f"[AlertManager] Callback error for {event}: {e}")
        except Exception as e:
            carb.log_error(f"[AlertManager] Failed to trigger callbacks: {e}")

    def shutdown(self) -> None:
        """Shutdown the alert manager"""
        self._alerts.clear()
        self._callbacks.clear()
        carb.log_info("[AlertManager] Shutdown complete") 