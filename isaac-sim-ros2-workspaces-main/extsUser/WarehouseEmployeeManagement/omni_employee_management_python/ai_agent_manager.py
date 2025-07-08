import carb
import aiohttp
import asyncio
import json
import websockets
from typing import Dict, Any, Optional, List, Callable
from .global_variables import DEFAULT_API_BASE_URL, DEFAULT_WEBSOCKET_URL


class AIAgentManager:
    """
    Manages AI agent integration with FastAPI backend
    Follows AgentIQ-compatible patterns for NVIDIA ecosystem integration
    """

    def __init__(self):
        self.settings = carb.settings.get_settings()
        # self.api_base_url = DEFAULT_API_BASE_URL
        # self.websocket_url = DEFAULT_WEBSOCKET_URL
        self.api_base_url = "http://localhost:1234"  # Changed from 8080 to 1234
        self.websocket_url = "ws://localhost:1234/ws"
        self.session = None
        self.websocket = None
        self.connected = False
        self.agents = {}

        # Agent types supported - ADD WAREHOUSE EMPLOYEE MANAGEMENT
        self.agent_types = {
            "warehouse_employee_management": {
                "endpoint": "/chat",  # AgentIQ standard endpoint
                "description": "Tracks warehouse employee positions and bounding boxes",
            },
            "workforce_optimizer": {
                "endpoint": "/agents/workforce/optimize",
                "description": "Optimizes workforce allocation and scheduling",
            },
            "safety_analyzer": {
                "endpoint": "/agents/safety/analyze",
                "description": "Analyzes safety compliance and risks",
            },
            "performance_predictor": {
                "endpoint": "/agents/performance/predict",
                "description": "Predicts performance metrics and trends",
            },
            "task_scheduler": {
                "endpoint": "/agents/tasks/schedule",
                "description": "Schedules and assigns tasks to employees",
            },
            "anomaly_detector": {
                "endpoint": "/agents/anomaly/detect",
                "description": "Detects anomalies in workforce behavior",
            },
        }

    def configure_for_aiq_toolkit(self, host="localhost", port=1234):
        """Configure AI Agent Manager for AIQ Toolkit connection"""
        self.api_base_url = f"http://{host}:{port}"
        self.websocket_url = f"ws://{host}:{port}/ws"
        
        carb.log_info(f"AI Agent Manager: Configured for AIQ Toolkit at {self.api_base_url}")
        
        # Store in settings
        self.settings.set_string("/persistent/exts/omni.employee_management/api_base_url", self.api_base_url)
        self.settings.set_string("/persistent/exts/omni.employee_management/websocket_url", self.websocket_url)

    async def initialize_connection(self) -> bool:
        """Initialize connection to AI backend"""
        try:
            # Initialize HTTP session
            self.session = aiohttp.ClientSession()

            # Test connection
            async with self.session.get(f"{self.api_base_url}/warehouse/health") as response:
                if response.status == 200:
                    self.connected = True
                    carb.log_info("AI Agent Manager: Connection established")
                    return True
                else:
                    carb.log_error(
                        f"AI Agent Manager: Health check failed with status {response.status}"
                    )
                    return False

        except Exception as e:
            carb.log_error(
                f"AI Agent Manager: Failed to initialize connection: {str(e)}"
            )
            return False

    async def connect_websocket(self) -> bool:
        """Connect to WebSocket for real-time updates"""
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            carb.log_info("AI Agent Manager: WebSocket connected")
            return True
        except Exception as e:
            carb.log_error(f"AI Agent Manager: WebSocket connection failed: {str(e)}")
            return False

    async def call_agent(
        self, agent_type: str, payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Call an AI agent with AgentIQ-compatible patterns

        Args:
            agent_type: Type of agent to call
            payload: Data to send to the agent

        Returns:
            Agent response or None if failed
        """
        if not self.connected or not self.session:
            carb.log_error("AI Agent Manager: Not connected to backend")
            return None

        if agent_type not in self.agent_types:
            carb.log_error(f"AI Agent Manager: Unknown agent type: {agent_type}")
            return None

        try:
            endpoint = self.agent_types[agent_type]["endpoint"]
            url = f"{self.api_base_url}{endpoint}"

            # Standard AgentIQ payload structure
            request_payload = {
                "agent_id": agent_type,
                "session_id": self._get_session_id(),
                "timestamp": self._get_timestamp(),
                "data": payload,
                "context": {
                    "environment": "isaac_sim",
                    "extension": "employee_management",
                    "version": "1.0.0",
                },
            }

            async with self.session.post(url, json=request_payload) as response:
                if response.status == 200:
                    result = await response.json()
                    carb.log_info(
                        f"AI Agent Manager: Agent {agent_type} call successful"
                    )
                    return result
                else:
                    error_text = await response.text()
                    carb.log_error(
                        f"AI Agent Manager: Agent {agent_type} call failed: {error_text}"
                    )
                    return None

        except Exception as e:
            carb.log_error(
                f"AI Agent Manager: Error calling agent {agent_type}: {str(e)}"
            )
            return None

    async def optimize_workforce(
        self, employee_data: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Call workforce optimization agent"""
        payload = {
            "employees": employee_data,
            "optimization_goals": ["efficiency", "safety", "cost"],
            "constraints": {
                "max_shift_hours": 8,
                "required_skills": [],
                "safety_requirements": True,
            },
        }
        return await self.call_agent("workforce_optimizer", payload)

    async def analyze_safety(
        self, safety_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Call safety analysis agent"""
        payload = {
            "safety_events": safety_data.get("events", []),
            "compliance_status": safety_data.get("compliance", {}),
            "risk_factors": safety_data.get("risks", []),
            "analysis_type": "real_time",
        }
        return await self.call_agent("safety_analyzer", payload)

    async def predict_performance(
        self, performance_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Call performance prediction agent"""
        payload = {
            "historical_data": performance_data.get("history", []),
            "current_metrics": performance_data.get("current", {}),
            "prediction_horizon": "1_day",
            "metrics_to_predict": ["productivity", "efficiency", "quality"],
        }
        return await self.call_agent("performance_predictor", payload)

    async def schedule_tasks(
        self, task_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Call task scheduling agent"""
        payload = {
            "tasks": task_data.get("tasks", []),
            "employees": task_data.get("employees", []),
            "constraints": task_data.get("constraints", {}),
            "optimization_criteria": [
                "completion_time",
                "resource_utilization",
                "skill_match",
            ],
        }
        return await self.call_agent("task_scheduler", payload)

    async def detect_anomalies(
        self, behavioral_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Call anomaly detection agent"""
        payload = {
            "behavioral_patterns": behavioral_data.get("patterns", []),
            "baseline_data": behavioral_data.get("baseline", {}),
            "detection_sensitivity": "medium",
            "anomaly_types": ["performance", "safety", "behavior"],
        }
        return await self.call_agent("anomaly_detector", payload)

    async def send_realtime_data(self, data: Dict[str, Any]) -> bool:
        """Send real-time data via WebSocket"""
        if not self.websocket:
            return False

        try:
            message = {
                "type": "realtime_update",
                "timestamp": self._get_timestamp(),
                "data": data,
            }
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            carb.log_error(f"AI Agent Manager: Failed to send real-time data: {str(e)}")
            return False

    def set_api_config(self, base_url: str, websocket_url: str = None):
        """Configure API endpoints"""
        self.api_base_url = base_url
        if websocket_url:
            self.websocket_url = websocket_url

        # Store in settings
        self.settings.set_string(
            "/persistent/exts/omni.employee_management/api_base_url", base_url
        )
        if websocket_url:
            self.settings.set_string(
                "/persistent/exts/omni.employee_management/websocket_url", websocket_url
            )

    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent manager status"""
        return {
            "connected": self.connected,
            "api_url": self.api_base_url,
            "websocket_url": self.websocket_url,
            "available_agents": list(self.agent_types.keys()),
            "session_active": self.session is not None,
            "websocket_active": self.websocket is not None,
        }

    # async def get_warehouse_employee_positions(self) -> Optional[Dict[str, Any]]:
    #     """
    #     Get employee positions via dedicated structured API endpoint
    #     Returns structured JSON data instead of chat responses
    #     """
    #     if not self.connected or not self.session:
    #         carb.log_error("AI Agent Manager: Not connected to backend")
    #         return None

    #     try:
    #         # url = f"{self.api_base_url}/warehouse/employees/positions"
    #         url = f"{self.api_base_url}/chat"


    #         async with self.session.get(url) as response:
    #             if response.status == 200:
    #                 result = await response.json()
    #                 carb.log_info(
    #                     "AI Agent Manager: Employee positions retrieved successfully via structured API"
    #                 )
    #                 return result
    #             else:
    #                 error_text = await response.text()
    #                 carb.log_error(
    #                     f"AI Agent Manager: Failed to get employee positions: {response.status} - {error_text}"
    #                 )
    #                 return None
    #     except Exception as e:
    #         carb.log_error(
    #             f"AI Agent Manager: Error getting employee positions: {str(e)}"
    #         )
    #         return None

    async def get_warehouse_employee_positions(self) -> Optional[Dict[str, Any]]:
        """Get employee positions via both structured and chat APIs"""
        if not self.connected or not self.session:
            carb.log_error("AI Agent Manager: Not connected to backend")
            return None

        try:
            # First try the structured API endpoint
            structured_url = f"{self.api_base_url}/warehouse/employees/positions"
            
            async with self.session.get(structured_url) as response:
                if response.status == 200:
                    result = await response.json()
                    carb.log_info("AI Agent Manager: Employee positions retrieved via structured API")
                    return result
                else:
                    carb.log_warn(f"Structured API failed: {response.status}, trying chat API")
            
            # Fallback to chat API
            chat_url = f"{self.api_base_url}/chat"
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": "Get current employee positions and bounding boxes from the warehouse"
                    }
                ]
            }

            async with self.session.post(chat_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    carb.log_info("AI Agent Manager: Employee positions retrieved via chat API")
                    
                    # Parse chat response
                    if "messages" in result and len(result["messages"]) > 0:
                        content = result["messages"][-1].get("content", "")
                        try:
                            import json
                            employee_data = json.loads(content)
                            return employee_data
                        except json.JSONDecodeError:
                            return {"status": "success", "raw_response": content}
                    
                    return result
                else:
                    error_text = await response.text()
                    carb.log_error(f"AI Agent Manager: Both APIs failed: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            carb.log_error(f"AI Agent Manager: Error getting employee positions: {str(e)}")
            return None

    async def update_warehouse_positions_to_sim(self) -> Optional[Dict[str, Any]]:
        """
        Update employee positions to Isaac Sim via structured API
        """
        if not self.connected or not self.session:
            carb.log_error("AI Agent Manager: Not connected to backend")
            return None

        try:
            # First get current positions
            positions = await self.get_warehouse_employee_positions()
            if not positions:
                return None

            # Send update request with structured data
            url = f"{self.api_base_url}/warehouse/employees/update"

            async with self.session.post(url, json=positions) as response:
                if response.status == 200:
                    result = await response.json()
                    carb.log_info(
                        "AI Agent Manager: Isaac Sim positions updated successfully"
                    )
                    return result
                else:
                    error_text = await response.text()
                    carb.log_error(
                        f"AI Agent Manager: Failed to update Isaac Sim: {response.status} - {error_text}"
                    )
                    return None

        except Exception as e:
            carb.log_error(f"AI Agent Manager: Error updating Isaac Sim: {str(e)}")
            return None

    async def get_warehouse_zone_status(self) -> Optional[Dict[str, Any]]:
        """
        Get warehouse zone occupancy status via structured API
        """
        if not self.connected or not self.session:
            carb.log_error("AI Agent Manager: Not connected to backend")
            return None

        try:
            url = f"{self.api_base_url}/warehouse/zones/status"

            async with self.session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    carb.log_info(
                        "AI Agent Manager: Zone status retrieved successfully"
                    )
                    return result
                else:
                    error_text = await response.text()
                    carb.log_error(
                        f"AI Agent Manager: Failed to get zone status: {response.status} - {error_text}"
                    )
                    return None
        except Exception as e:
            carb.log_error(f"AI Agent Manager: Error getting zone status: {str(e)}")
            return None

    # ADD method to handle incoming position updates from the agent
    async def handle_warehouse_employee_update(
        self, employee_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle employee position updates from the warehouse agent."""
        try:
            carb.log_info(f"AI Agent Manager: Received employee data: {employee_data}")

            # Process the employee data and update Isaac Sim
            if "employees" in employee_data:
                for employee in employee_data["employees"]:
                    emp_id = employee.get("id", "unknown")
                    position = employee.get("position", [0, 0, 0])
                    bbox = employee.get("bounding_box", [0, 0, 0, 0])
                    zone = employee.get("zone", "unassigned")
                    confidence = employee.get("confidence", 0.0)

                    carb.log_info(
                        f"AI Agent Manager: Employee {emp_id} at position {position} in {zone} (confidence: {confidence})"
                    )

                    # Here you would update your Isaac Sim scene
                    # This is where you'd call your motion_capture_manager

            return {
                "status": "success",
                "updated_count": len(employee_data.get("employees", [])),
            }
        except Exception as e:
            carb.log_error(
                f"AI Agent Manager: Error handling employee update: {str(e)}"
            )
            return {"status": "error", "message": str(e)}

    async def shutdown(self):
        """Cleanup connections"""
        try:
            if self.websocket:
                await self.websocket.close()
                self.websocket = None

            if self.session:
                await self.session.close()
                self.session = None

            self.connected = False
            carb.log_info("AI Agent Manager: Shutdown complete")

        except Exception as e:
            carb.log_error(f"AI Agent Manager: Error during shutdown: {str(e)}")

    def _get_session_id(self) -> str:
        """Generate or retrieve session ID"""
        session_id = self.settings.get_string(
            "/persistent/exts/omni.employee_management/session_id"
        )
        if not session_id:
            import uuid

            session_id = str(uuid.uuid4())
            self.settings.set_string(
                "/persistent/exts/omni.employee_management/session_id", session_id
            )
        return session_id

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        import datetime

        return datetime.datetime.now().isoformat()
