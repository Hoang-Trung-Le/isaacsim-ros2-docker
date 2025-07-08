"""
OmniAlert Window - Simplified Main UI for Industrial Alert System
"""

import omni.ui as ui
import omni.kit.notification_manager as nm
import carb
import asyncio
import threading
import requests
from typing import Optional, List

from .alert_types import (
    Alert,
    AlertSeverity,
    AlertCategory,
    AlertStatus,
    AlertLocation,
)
from .camera_controller import CameraController

# Origin to USD Prim Path mapping for Industrial Alert Agent
ORIGIN_TO_PRIM_PATH = {
    "Worker_1": "/World/Worker_01",
    "Worker_2": "/World/Worker_02", 
    "Worker_3": "/World/Worker_03",
    "Conveyor_1": "/World/Warehouse/Conveyor_001",
    "Conveyor_2": "/World/Warehouse/Conveyor_002",
    "Conveyor_3": "/World/Warehouse/Conveyor_003",
    "Equipment_1": "/World/Equipment/Device_01",
    "Equipment_2": "/World/Equipment/Device_02",
    "Pump_P101": "/World/Equipment/Pump_P101",
    "Zone_A": "/World/Warehouse/Zone_A",
    "Zone_B": "/World/Warehouse/Zone_B",
    "Zone_C": "/World/Warehouse/Zone_C",
    "ProductionLine_A": "/World/Warehouse/ProductionLine_A",
    "ProductionLine_B": "/World/Warehouse/ProductionLine_B",
}


class OmniAlertWindow(ui.Window):
    """Simplified OmniAlert window with Industrial Alert Agent integration"""

    def __init__(self, title: str = "OmniAlert - Industrial Alert System", **kwargs):
        super().__init__(title, **kwargs)

        # Core components
        self.camera_controller = CameraController()
        self._industrial_agent_url = "http://localhost:1234"
        
        # UI state
        self._connection_status = "Disconnected"
        self._last_alert_count = 0
        
        # Build the UI
        self._build_window()

        carb.log_info("[OmniAlertWindow] Window initialized")

    def _build_window(self):
        """Build the main window UI"""
        with self.frame:
            with ui.VStack():
                # Header
                ui.Label("OmniAlert - Industrial Alert System", 
                        style={"font_size": 18, "color": 0xFFFFFFFF})
                
                # Status
                self._status_label = ui.Label(f"Status: {self._connection_status}", 
                                            style={"font_size": 12, "color": 0xFFCCCCCC})
                
                # Main button to fetch alerts
                ui.Button("Fetch Alerts from Industrial Agent", 
                         clicked_fn=self._fetch_and_show_alerts,
                         height=40,
                         style={"background_color": 0xFF2E5D8E, "font_size": 14})
                
                ui.Spacer(height=10)
                
                # Test section
                with ui.CollapsableFrame("Test Controls"):
                    with ui.VStack(spacing=10):
                        ui.Button("Test Notification", 
                                 clicked_fn=self._test_notification,
                                 style={"background_color": 0xFF4CAF50})
                        
                        ui.Button("Test Camera Navigation", 
                                 clicked_fn=self._test_camera_navigation,
                                 style={"background_color": 0xFF4CAF50})

    def _fetch_and_show_alerts(self):
        """Fetch alerts from industrial agent and show notifications"""
        carb.log_info("[OmniAlertWindow] Fetching alerts...")
        
        # Run in a separate thread to avoid blocking UI
        def fetch_thread():
            try:
                url = f"{self._industrial_agent_url}/industrial_alert/alerts"
                response = requests.get(url, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "success" and "alerts" in data:
                        alerts = data["alerts"]
                        carb.log_info(f"[OmniAlertWindow] Fetched {len(alerts)} alerts")
                        
                        # Update status on main thread
                        self._connection_status = "Connected"
                        self._last_alert_count = len(alerts)
                        self._update_status_ui()
                        
                        # Show notifications for alerts
                        self._show_alert_notifications(alerts)
                        
                    else:
                        carb.log_warn(f"[OmniAlertWindow] No alerts in response: {data}")
                        nm.post_notification("No alerts found", duration=2)
                        
                else:
                    carb.log_warn(f"[OmniAlertWindow] Response status: {response.status_code}")
                    nm.post_notification(f"Server error: {response.status_code}", 
                                       status=nm.NotificationStatus.WARNING)
                    self._connection_status = f"Error {response.status_code}"
                    self._update_status_ui()

            except Exception as e:
                carb.log_error(f"[OmniAlertWindow] Failed to fetch alerts: {e}")
                nm.post_notification(f"Connection failed: {str(e)}", 
                                   status=nm.NotificationStatus.WARNING)
                self._connection_status = "Connection Failed"
                self._update_status_ui()
        
        # Start the fetch in a background thread
        thread = threading.Thread(target=fetch_thread)
        thread.daemon = True
        thread.start()

    def _update_status_ui(self):
        """Update the status label"""
        if hasattr(self, '_status_label'):
            status_text = f"Status: {self._connection_status}"
            if self._last_alert_count > 0:
                status_text += f" | Alerts: {self._last_alert_count}"
            self._status_label.text = status_text

    def _show_alert_notifications(self, alerts_data: List):
        """Show notifications for fetched alerts"""
        try:
            for alert_data in alerts_data:
                # Convert to Alert object
                alert = self._convert_industrial_alert(alert_data)
                
                # Determine notification status based on severity
                notification_status = nm.NotificationStatus.INFO
                if alert.severity == AlertSeverity.CRITICAL:
                    notification_status = nm.NotificationStatus.WARNING
                elif alert.severity == AlertSeverity.HIGH:
                    notification_status = nm.NotificationStatus.WARNING
                
                # Create notification with action button
                def create_view_callback(alert_obj):
                    return lambda: self._navigate_to_alert(alert_obj)
                
                view_button = nm.NotificationButtonInfo(
                    "View Location", 
                    on_complete=create_view_callback(alert)
                )
                
                ack_button = nm.NotificationButtonInfo(
                    "Acknowledge",
                    on_complete=lambda: carb.log_info(f"Acknowledged alert {alert.id}")
                )
                
                # Show notification
                nm.post_notification(
                    f"[{alert.severity.value.upper()}] {alert.title}",
                    duration=8,
                    status=notification_status,
                    button_infos=[view_button, ack_button],
                    hide_after_timeout=False
                )
                
                carb.log_info(f"[OmniAlertWindow] Showed notification for alert: {alert.id}")
                
        except Exception as e:
            carb.log_error(f"[OmniAlertWindow] Error showing notifications: {e}")

    def _convert_industrial_alert(self, data: dict) -> Alert:
        """Convert industrial agent alert data to Alert object"""
        # Parse location from origin
        origin = data.get("origin", "")
        prim_path = ORIGIN_TO_PRIM_PATH.get(origin)
        
        location = None
        if prim_path:
            location = AlertLocation(
                x=0.0, y=0.0, z=0.0,
                prim_path=prim_path
            )
        
        return Alert(
            id=data.get("id", "unknown"),
            title=data.get("title", "Industrial Alert"),
            message=data.get("description", ""),
            severity=AlertSeverity(data.get("severity", "medium")),
            category=AlertCategory(data.get("category", "system")),
            status=AlertStatus(data.get("status", "active")),
            location=location,
            source="industrial_agent",
            # Legacy fields
            description=data.get("description", ""),
            origin=origin,
            created_at=data.get("created_at", ""),
        )

    def _navigate_to_alert(self, alert: Alert):
        """Navigate camera to alert location"""
        try:
            if alert.location and alert.location.prim_path:
                carb.log_warn(f"[OmniAlertWindow] Navigating to: {alert.location.prim_path}")
                self.camera_controller.focus_on_prim(alert.location.prim_path)
                
                # # Run camera navigation in a thread to handle async calls safely
                # def nav_thread():
                #     try:
                #         # Create new event loop for this thread
                #         loop = asyncio.new_event_loop()
                #         asyncio.set_event_loop(loop)
                        
                #         # Run the navigation
                #         if alert.location.prim_path:
                #             loop.run_until_complete(
                #                 self.camera_controller.focus_on_prim(alert.location.prim_path)
                #             )
                        
                #         loop.close()
                        
                #     except Exception as e:
                #         carb.log_error(f"[OmniAlertWindow] Navigation thread error: {e}")
                
                # thread = threading.Thread(target=nav_thread)
                # thread.daemon = True
                # thread.start()
                
                nm.post_notification(f"Navigating to {alert.origin}", duration=3)
            else:
                carb.log_warn(f"[OmniAlertWindow] No location data for alert: {alert.id}")
                nm.post_notification("No location data for this alert", duration=3)
                
        except Exception as e:
            carb.log_error(f"[OmniAlertWindow] Error navigating to alert: {e}")
            nm.post_notification(f"Navigation error: {str(e)}", 
                               status=nm.NotificationStatus.WARNING)

    def _test_notification(self):
        """Test notification system"""
        carb.log_warn(f"[OmniAlertWindow] Testing notification")
        nm.post_notification(
            "Test Alert: Equipment Temperature High",
            duration=5,
            status=nm.NotificationStatus.WARNING,
            button_infos=[
                nm.NotificationButtonInfo("View", on_complete=lambda: carb.log_warn("Test view clicked")),
                nm.NotificationButtonInfo("OK", on_complete=lambda: carb.log_warn("Test OK clicked"))
            ]
        )

    def _test_camera_navigation(self):
        """Test camera navigation to Worker"""
        try:
            prim_path = "/World/Worker_01"  # Default worker path
            carb.log_warn(f"[OmniAlertWindow] Testing navigation to: {prim_path}")
            self.camera_controller.focus_on_prim(prim_path)
            
            # # Run navigation in a thread
            # def test_nav_thread():
            #     try:
            #         loop = asyncio.new_event_loop()
            #         asyncio.set_event_loop(loop)
                    
            #         loop.run_until_complete(
            #             self.camera_controller.focus_on_prim(prim_path)
            #         )
                    
            #         loop.close()
                    
            #     except Exception as e:
            #         carb.log_error(f"[OmniAlertWindow] Test navigation thread error: {e}")
            
            # thread = threading.Thread(target=test_nav_thread)
            # thread.daemon = True
            # thread.start()
            
            nm.post_notification(f"Testing navigation to {prim_path}", duration=3)
            
        except Exception as e:
            carb.log_error(f"[OmniAlertWindow] Error in test navigation: {e}")
            nm.post_notification(f"Test navigation error: {str(e)}", 
                               status=nm.NotificationStatus.WARNING)

    def destroy(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'camera_controller'):
                self.camera_controller.shutdown()
            
            super().destroy()
            carb.log_info("[OmniAlertWindow] Window destroyed")
            
        except Exception as e:
            carb.log_error(f"[OmniAlertWindow] Error during cleanup: {e}")
