"""
API Client for OmniAlert Extension
Enhanced client for fetching industrial alerts with polling and callbacks
"""

import asyncio
import aiohttp
import carb
from typing import List, Optional, Callable, Dict, Any

from .alert_types import Alert

# Origin to USD Prim Path mapping for Industrial Alert Agent
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


class AlertAPIClient:
    """Enhanced API client for fetching industrial alerts with polling support"""

    def __init__(self):
        self._industrial_agent_url = "http://localhost:1234"
        self._session: Optional[aiohttp.ClientSession] = None
        self._polling_enabled = False
        self._polling_task: Optional[asyncio.Task] = None
        self._polling_interval = 10.0
        
        # Callbacks
        self._alert_callback: Optional[Callable] = None
        self._connection_callback: Optional[Callable] = None
        
        # State
        self._last_fetch_count = 0
        self._known_alert_ids: set = set()
        
        carb.log_info("[AlertAPIClient] Initialized")

    def configure_industrial_agent(self, url: str, enabled: bool = True) -> None:
        """Configure the industrial agent connection"""
        self._industrial_agent_url = url
        carb.log_info(f"[AlertAPIClient] Configured industrial agent: {url}")

    def set_alert_callback(self, callback: Callable) -> None:
        """Set callback for new alerts"""
        self._alert_callback = callback
        carb.log_info("[AlertAPIClient] Alert callback set")

    def set_connection_callback(self, callback: Callable) -> None:
        """Set callback for connection status changes"""
        self._connection_callback = callback
        carb.log_info("[AlertAPIClient] Connection callback set")

    async def initialize_session(self) -> bool:
        """Initialize HTTP session"""
        try:
            if self._session:
                await self._session.close()

            timeout = aiohttp.ClientTimeout(total=30.0)
            self._session = aiohttp.ClientSession(timeout=timeout)

            carb.log_info("[AlertAPIClient] Session initialized")
            
            # Notify connection status
            if self._connection_callback:
                self._connection_callback(True)
            
            return True
        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Failed to initialize session: {e}")
            
            # Notify connection failure
            if self._connection_callback:
                self._connection_callback(False)
            
            return False

    async def fetch_industrial_alerts(self) -> List[Alert]:
        """Fetch alerts from Industrial Alert Agent"""
        if not self._session:
            await self.initialize_session()

        try:
            url = f"{self._industrial_agent_url}/industrial_alert/alerts"

            async with self._session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    if data.get("status") == "success" and "alerts" in data:
                        industrial_alerts = data["alerts"]
                        alerts = []

                        for alert_data in industrial_alerts:
                            alert = Alert.from_industrial_data(alert_data)
                            alerts.append(alert)

                        carb.log_info(f"[AlertAPIClient] Fetched {len(alerts)} alerts")
                        self._last_fetch_count = len(alerts)
                        return alerts
                    else:
                        carb.log_warn(
                            f"[AlertAPIClient] No alerts in response: {data}"
                        )
                        return []
                else:
                    carb.log_warn(
                        f"[AlertAPIClient] Response status: {response.status}"
                    )
                    return []

        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Failed to fetch alerts: {e}")
            
            # Notify connection failure
            if self._connection_callback:
                self._connection_callback(False)
            
            return []

    def start_polling(self, interval: float = 10.0) -> bool:
        """Start polling for alerts"""
        try:
            if self._polling_enabled:
                carb.log_warn("[AlertAPIClient] Polling already started")
                return True

            self._polling_interval = interval
            self._polling_enabled = True
            self._polling_task = asyncio.create_task(self._polling_loop())
            
            carb.log_info(f"[AlertAPIClient] Started polling with interval: {interval}s")
            return True
            
        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Failed to start polling: {e}")
            return False

    def stop_polling(self) -> None:
        """Stop polling for alerts"""
        try:
            if not self._polling_enabled:
                carb.log_warn("[AlertAPIClient] Polling not active")
                return

            self._polling_enabled = False
            
            if self._polling_task:
                self._polling_task.cancel()
                self._polling_task = None

            carb.log_info("[AlertAPIClient] Stopped polling")
            
        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Error stopping polling: {e}")

    async def _polling_loop(self) -> None:
        """Main polling loop"""
        try:
            while self._polling_enabled:
                # Fetch alerts
                alerts = await self.fetch_industrial_alerts()
                
                # Filter for new alerts
                new_alerts = []
                for alert in alerts:
                    if alert.id not in self._known_alert_ids:
                        new_alerts.append(alert)
                        self._known_alert_ids.add(alert.id)
                
                # Notify callback of new alerts
                if new_alerts and self._alert_callback:
                    self._alert_callback(new_alerts)
                
                # Wait for next poll
                await asyncio.sleep(self._polling_interval)
                
        except asyncio.CancelledError:
            carb.log_info("[AlertAPIClient] Polling loop cancelled")
        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Error in polling loop: {e}")

    async def send_alert_action(self, alert_id: str, action: str, data: Dict[str, Any] = None) -> bool:
        """Send action for an alert to the industrial agent"""
        try:
            if not self._session:
                await self.initialize_session()

            url = f"{self._industrial_agent_url}/industrial_alert/alerts/{alert_id}/{action}"
            payload = data or {}

            async with self._session.post(url, json=payload) as response:
                if response.status == 200:
                    carb.log_info(f"[AlertAPIClient] Sent action '{action}' for alert: {alert_id}")
                    return True
                else:
                    carb.log_warn(f"[AlertAPIClient] Action failed with status: {response.status}")
                    return False

        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Failed to send action: {e}")
            return False

    def get_prim_path_for_origin(self, origin: str) -> Optional[str]:
        """Get USD prim path for alert origin"""
        return ORIGIN_TO_PRIM_PATH.get(origin)

    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        return {
            "connected": self._session is not None,
            "polling_enabled": self._polling_enabled,
            "polling_interval": self._polling_interval,
            "last_fetch_count": self._last_fetch_count,
            "known_alerts": len(self._known_alert_ids),
            "industrial_agent_url": self._industrial_agent_url
        }

    async def shutdown(self) -> None:
        """Shutdown API client"""
        try:
            # Stop polling
            self.stop_polling()
            
            # Close session
            if self._session:
                await self._session.close()
                self._session = None

            # Clear state
            self._known_alert_ids.clear()
            
            carb.log_info("[AlertAPIClient] Shutdown complete")
            
        except Exception as e:
            carb.log_error(f"[AlertAPIClient] Error during shutdown: {e}")


# Alias for backward compatibility
SimpleAPIClient = AlertAPIClient
