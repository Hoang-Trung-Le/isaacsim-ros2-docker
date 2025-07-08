"""
Notification System for OmniAlert Extension
Manages popup notifications and sound alerts
"""

import carb
import omni.ui as ui
from typing import List, Callable, Optional
from .alert_types import Alert, AlertSeverity


class NotificationPopup:
    """Individual notification popup"""

    def __init__(self, alert: Alert, on_click_callback: Optional[Callable] = None):
        self.alert = alert
        self.on_click_callback = on_click_callback
        self.window: Optional[ui.Window] = None
        self._create_popup()

    def _create_popup(self):
        """Create the popup window"""
        try:
            # Determine colors based on severity
            colors = {
                AlertSeverity.CRITICAL: 0xFFFF4444,
                AlertSeverity.HIGH: 0xFFFF8800,
                AlertSeverity.MEDIUM: 0xFFFFDD00,
                AlertSeverity.LOW: 0xFF44AAFF,
                AlertSeverity.INFO: 0xFF888888,
            }
            
            bg_color = colors.get(self.alert.severity, 0xFF888888)
            
            # Create popup window
            self.window = ui.Window(
                f"Alert: {self.alert.id}",
                width=320,
                height=120,
                flags=ui.WINDOW_FLAGS_NO_RESIZE | ui.WINDOW_FLAGS_NO_MOVE,
            )
            
            with self.window.frame:
                with ui.VStack(spacing=5):
                    # Header with severity indicator
                    with ui.HStack(height=25):
                        ui.Rectangle(width=4, style={"background_color": bg_color})
                        ui.Label(
                            f"[{self.alert.severity.value.upper()}] {self.alert.title}",
                            style={"font_size": 14, "color": 0xFFFFFFFF}
                        )
                        ui.Spacer()
                        
                        # Close button
                        ui.Button(
                            "✕",
                            width=20,
                            height=20,
                            clicked_fn=self.close,
                            style={"background_color": 0x00000000}
                        )
                    
                    # Message
                    ui.Label(
                        self.alert.message,
                        word_wrap=True,
                        style={"font_size": 12, "color": 0xFFCCCCCC}
                    )
                    
                    # Action buttons
                    with ui.HStack():
                        if self.on_click_callback:
                            ui.Button(
                                "🔍 View Location",
                                clicked_fn=self._on_view_clicked,
                                style={"background_color": 0xFF2E5D8E}
                            )
                        
                        ui.Button(
                            "✓ Acknowledge",
                            clicked_fn=self._on_acknowledge_clicked,
                            style={"background_color": 0xFF2E8E5D}
                        )

            carb.log_info(f"[NotificationPopup] Created popup for alert: {self.alert.id}")

        except Exception as e:
            carb.log_error(f"[NotificationPopup] Failed to create popup: {e}")

    def _on_view_clicked(self):
        """Handle view button click"""
        try:
            if self.on_click_callback:
                self.on_click_callback(self.alert)
            self.close()
        except Exception as e:
            carb.log_error(f"[NotificationPopup] Error in view click: {e}")

    def _on_acknowledge_clicked(self):
        """Handle acknowledge button click"""
        try:
            # Just acknowledge and close for now
            carb.log_info(f"[NotificationPopup] Acknowledged alert: {self.alert.id}")
            self.close()
        except Exception as e:
            carb.log_error(f"[NotificationPopup] Error in acknowledge click: {e}")

    def close(self):
        """Close the popup"""
        try:
            if self.window:
                self.window.destroy()
                self.window = None
                carb.log_info(f"[NotificationPopup] Closed popup for alert: {self.alert.id}")
        except Exception as e:
            carb.log_error(f"[NotificationPopup] Error closing popup: {e}")


class NotificationSystem:
    """Manages notification popups"""

    def __init__(self):
        self._active_notifications: List[NotificationPopup] = []
        self._max_notifications = 5
        self._click_callbacks: List[Callable] = []
        carb.log_info("[NotificationSystem] Initialized")

    def show_notification(self, alert: Alert) -> None:
        """Show a notification for an alert"""
        try:
            # Remove old notifications if at limit
            while len(self._active_notifications) >= self._max_notifications:
                old_notification = self._active_notifications.pop(0)
                old_notification.close()

            # Create new notification
            notification = NotificationPopup(alert, self._on_notification_clicked)
            self._active_notifications.append(notification)
            
            carb.log_info(f"[NotificationSystem] Showed notification for: {alert.id}")

        except Exception as e:
            carb.log_error(f"[NotificationSystem] Failed to show notification: {e}")

    def _on_notification_clicked(self, alert: Alert) -> None:
        """Handle notification click"""
        try:
            # Trigger all click callbacks
            for callback in self._click_callbacks:
                callback(alert)
        except Exception as e:
            carb.log_error(f"[NotificationSystem] Error in click callbacks: {e}")

    def add_click_callback(self, callback: Callable) -> None:
        """Add a callback for notification clicks"""
        self._click_callbacks.append(callback)
        carb.log_info("[NotificationSystem] Added click callback")

    def remove_click_callback(self, callback: Callable) -> None:
        """Remove a click callback"""
        if callback in self._click_callbacks:
            self._click_callbacks.remove(callback)
            carb.log_info("[NotificationSystem] Removed click callback")

    def clear_all_notifications(self) -> None:
        """Clear all active notifications"""
        try:
            for notification in self._active_notifications:
                notification.close()
            self._active_notifications.clear()
            carb.log_info("[NotificationSystem] Cleared all notifications")
        except Exception as e:
            carb.log_error(f"[NotificationSystem] Error clearing notifications: {e}")

    def set_max_notifications(self, max_count: int) -> None:
        """Set maximum number of simultaneous notifications"""
        self._max_notifications = max(1, max_count)
        carb.log_info(f"[NotificationSystem] Set max notifications to: {self._max_notifications}")

    def shutdown(self) -> None:
        """Shutdown the notification system"""
        self.clear_all_notifications()
        self._click_callbacks.clear()
        carb.log_info("[NotificationSystem] Shutdown complete")


class NotificationManager:
    """High-level notification manager that coordinates with alert manager and camera controller"""

    def __init__(self, alert_manager, camera_controller):
        self.alert_manager = alert_manager
        self.camera_controller = camera_controller
        self.notification_system = NotificationSystem()
        
        # Configure notification system
        self.notification_system.add_click_callback(self._handle_notification_click)
        
        carb.log_info("[NotificationManager] Initialized")

    def _handle_notification_click(self, alert: Alert) -> None:
        """Handle notification click - navigate to location and acknowledge"""
        try:
            carb.log_info(f"[NotificationManager] Handling click for alert: {alert.id}")
            
            # Navigate to location if available
            if alert.location and alert.location.prim_path:
                import asyncio
                asyncio.create_task(
                    self.camera_controller.focus_on_prim(alert.location.prim_path)
                )
            
            # Acknowledge the alert
            self.alert_manager.acknowledge_alert(alert.id, "NotificationClick")
            
        except Exception as e:
            carb.log_error(f"[NotificationManager] Error handling notification click: {e}")

    def show_notification(self, alert: Alert) -> None:
        """Show notification (proxy to notification system)"""
        self.notification_system.show_notification(alert)

    def clear_all_notifications(self) -> None:
        """Clear all notifications (proxy to notification system)"""
        self.notification_system.clear_all_notifications()

    def shutdown(self) -> None:
        """Shutdown the notification manager"""
        self.notification_system.shutdown()
        carb.log_info("[NotificationManager] Shutdown complete") 