import omni.ui as ui
import carb
import json
import aiohttp
import asyncio
from typing import Dict, Any, Optional
from .global_variables import EXTENSION_TITLE, EXTENSION_DESCRIPTION
from .style import StyleSheet, get_style, STYLESHEET_LOADED
from .ai_agent_manager import AIAgentManager
from .motion_capture_manager import MotionCaptureManager
from .workforce_analytics_manager import WorkforceAnalyticsManager
from .safety_monitoring_manager import SafetyMonitoringManager
from .camera_calibration import CameraCalibrationManager
from .sync_ui_controller import SyncUIController


class EmployeeManagementWindow(ui.Window):
    """Main window for Employee Management System"""

    def __init__(self, title: str, **kwargs):
        super().__init__(title, **kwargs)

        # Initialize managers
        self.ai_agent_manager = AIAgentManager()
        self.motion_capture_manager = MotionCaptureManager()
        self.analytics_manager = WorkforceAnalyticsManager()
        self.safety_manager = SafetyMonitoringManager()
        self.calibration_manager = CameraCalibrationManager()
        
        # Initialize sync controller
        self.sync_controller = None

        # UI state
        self._style_sheet = StyleSheet() if STYLESHEET_LOADED else None
        self.system_status = {
            "ai_agents": False,
            "motion_capture": False,
            "analytics": False,
            "safety_monitoring": False,
            "camera_calibration": False,
            "isaac_sim_sync": False,
        }

        # Build window
        self.frame.set_build_fn(self._build_window)

        # Initialize systems
        self._initialize_systems()

    def _initialize_systems(self):
        """Initialize all subsystems"""
        try:
            # Initialize analytics
            self.analytics_manager.initialize_analytics()
            self.system_status["analytics"] = True

            # Initialize safety monitoring
            self.safety_manager.initialize_safety_monitoring()
            self.system_status["safety_monitoring"] = True

            # Initialize motion capture (async)
            asyncio.ensure_future(self._init_motion_capture())

            # Initialize AI agents (async)
            asyncio.ensure_future(self._init_ai_agents())

        except Exception as e:
            carb.log_error(
                f"Employee Management: Failed to initialize systems: {str(e)}"
            )

    async def _init_motion_capture(self):
        """Initialize motion capture system"""
        try:
            success = await self.motion_capture_manager.initialize_avatars_system()
            self.system_status["motion_capture"] = success
        except Exception as e:
            carb.log_error(f"Employee Management: Motion capture init failed: {str(e)}")

    async def _init_ai_agents(self):
        """Initialize AI agent system and sync controller"""
        try:
            # Configure for AIQ Toolkit before connecting
            self.ai_agent_manager.configure_for_aiq_toolkit(host="localhost", port=1234)
            
            success = await self.ai_agent_manager.initialize_connection()
            self.system_status["ai_agents"] = success
            
            if success:
                carb.log_info("Employee Management: Successfully connected to AIQ Toolkit")
                
                # Initialize sync controller after AI agent connection
                await self._init_sync_controller()
            else:
                carb.log_error("Employee Management: Failed to connect to AIQ Toolkit")
                
        except Exception as e:
            carb.log_error(f"Employee Management: AI agents init failed: {str(e)}")

    async def _init_sync_controller(self):
        """Initialize the Isaac Sim sync controller"""
        try:
            if not self.sync_controller:
                self.sync_controller = SyncUIController(
                    self.ai_agent_manager, 
                    self._style_sheet
                )
            
            # Initialize the sync system
            success = await self.sync_controller.initialize_async()
            self.system_status["isaac_sim_sync"] = success
            
            if success:
                carb.log_info("Employee Management: Isaac Sim sync controller initialized")
            else:
                carb.log_error("Employee Management: Failed to initialize sync controller")
                
        except Exception as e:
            carb.log_error(f"Employee Management: Sync controller init failed: {str(e)}")

    def _build_window(self):
        """Build the main UI window"""
        with ui.VStack(style=get_style(self._style_sheet, "window")):
            self._build_header()
            self._build_system_status()
            self._build_main_content()

    def _build_header(self):
        """Build window header"""
        with ui.HStack(
            height=60, style=get_style(self._style_sheet, "collapsable_frame")
        ):
            ui.Spacer(width=10)
            with ui.VStack():
                ui.Spacer(height=5)
                ui.Label(
                    "Employee Management System",
                    style=get_style(self._style_sheet, "label_large"),
                )
                ui.Label(
                    "Smart Warehouse & Factory Workforce Management",
                    style=get_style(self._style_sheet, "label_secondary"),
                )
                ui.Spacer(height=5)
            ui.Spacer()

    def _build_system_status(self):
        """Build system status panel"""
        with ui.CollapsableFrame(
            "System Status",
            height=0,
            collapsed=True,
            style=get_style(self._style_sheet, "collapsable_frame"),
        ):
            with ui.VStack(spacing=5):
                with ui.HStack(height=25):
                    ui.Label(
                        "AI Agents:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["ai_agents"]
                        else "status_error"
                    )
                    ui.Label(
                        (
                            "Connected"
                            if self.system_status["ai_agents"]
                            else "Disconnected"
                        ),
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "Configure",
                        width=80,
                        clicked_fn=self._show_ai_config_dialog,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

                with ui.HStack(height=25):
                    ui.Label(
                        "Isaac Sim Sync:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["isaac_sim_sync"]
                        else "status_error"
                    )
                    ui.Label(
                        (
                            "Ready"
                            if self.system_status["isaac_sim_sync"]
                            else "Not Ready"
                        ),
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "Configure",
                        width=80,
                        clicked_fn=self._show_sync_config,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

                with ui.HStack(height=25):
                    ui.Label(
                        "Motion Capture:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["motion_capture"]
                        else "status_error"
                    )
                    ui.Label(
                        (
                            "Active"
                            if self.system_status["motion_capture"]
                            else "Inactive"
                        ),
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "Setup",
                        width=80,
                        clicked_fn=self._show_motion_capture_setup,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

                with ui.HStack(height=25):
                    ui.Label(
                        "Analytics:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["analytics"]
                        else "status_error"
                    )
                    ui.Label(
                        "Running" if self.system_status["analytics"] else "Stopped",
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "View",
                        width=80,
                        clicked_fn=self._show_analytics_dashboard,
                        style=get_style(self._style_sheet, "button"),
                    )

                with ui.HStack(height=25):
                    ui.Label(
                        "Safety Monitor:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["safety_monitoring"]
                        else "status_error"
                    )
                    ui.Label(
                        (
                            "Monitoring"
                            if self.system_status["safety_monitoring"]
                            else "Offline"
                        ),
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "Monitor",
                        width=80,
                        clicked_fn=self._show_safety_dashboard,
                        style=get_style(self._style_sheet, "button_warning"),
                    )

                with ui.HStack(height=25):
                    ui.Label(
                        "Camera Calibration:",
                        width=120,
                        style=get_style(self._style_sheet, "label"),
                    )
                    status_style = (
                        "status_good"
                        if self.system_status["camera_calibration"]
                        else "status_warning"
                    )
                    ui.Label(
                        (
                            "Calibrated"
                            if self.system_status["camera_calibration"]
                            else "Needs Setup"
                        ),
                        style=get_style(self._style_sheet, status_style),
                    )
                    ui.Spacer()
                    ui.Button(
                        "Calibrate",
                        width=80,
                        clicked_fn=self._show_calibration_wizard,
                        style=get_style(self._style_sheet, "button"),
                    )

    def _build_main_content(self):
        """Build main content area"""
        with ui.VStack(spacing=5):
            self._build_quick_actions()
            self._build_employee_management()
            self._build_analytics_overview()
            self._build_safety_overview()
            self._build_sync_section()

    def _build_quick_actions(self):
        """Build quick actions panel"""
        with ui.CollapsableFrame(
            "Quick Actions",
            height=0,
            collapsed=False,
            style=get_style(self._style_sheet, "collapsable_frame"),
        ):
            with ui.HStack(spacing=10, height=40):
                ui.Button(
                    "Add Employee",
                    clicked_fn=self._add_employee_dialog,
                    style=get_style(self._style_sheet, "button_success"),
                )

                ui.Button(
                    "Start Tracking",
                    clicked_fn=self._start_tracking,
                    style=get_style(self._style_sheet, "button"),
                )

                ui.Button(
                    "Emergency Stop",
                    clicked_fn=self._emergency_stop,
                    style=get_style(self._style_sheet, "button_danger"),
                )

                ui.Button(
                    "Export Data",
                    clicked_fn=self._export_data,
                    style=get_style(self._style_sheet, "button_secondary"),
                )

    def _build_employee_management(self):
        """Build employee management panel"""
        with ui.CollapsableFrame(
            "Employee Management",
            height=0,
            collapsed=True,
            style=get_style(self._style_sheet, "collapsable_frame"),
        ):
            with ui.VStack(spacing=5):
                # Employee list
                with ui.HStack(height=25):
                    ui.Label(
                        "Active Employees:", style=get_style(self._style_sheet, "label")
                    )
                    ui.Spacer()
                    employee_count = len(
                        self.motion_capture_manager.get_employee_list()
                    )
                    ui.Label(
                        f"{employee_count}",
                        style=get_style(self._style_sheet, "metric_value"),
                    )

                # Employee actions
                with ui.HStack(spacing=5, height=30):
                    self._employee_id_field = ui.StringField(
                        style=get_style(self._style_sheet, "text_field")
                    )
                    self._employee_id_field.model.set_value("employee_001")

                    ui.Button(
                        "Add",
                        width=60,
                        clicked_fn=self._add_employee,
                        style=get_style(self._style_sheet, "button_success"),
                    )

                    ui.Button(
                        "Remove",
                        width=60,
                        clicked_fn=self._remove_employee,
                        style=get_style(self._style_sheet, "button_danger"),
                    )

                # Camera mapping
                ui.Separator(style=get_style(self._style_sheet, "separator"))
                ui.Label("Camera Mapping:", style=get_style(self._style_sheet, "label"))

                with ui.HStack(spacing=5, height=30):
                    self._camera_id_field = ui.StringField(
                        style=get_style(self._style_sheet, "text_field")
                    )
                    self._camera_id_field.model.set_value("camera_001")

                    ui.Button(
                        "Configure",
                        width=80,
                        clicked_fn=self._configure_camera,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

    def _build_analytics_overview(self):
        """Build analytics overview panel"""
        with ui.CollapsableFrame(
            "Analytics Overview",
            height=0,
            collapsed=True,
            style=get_style(self._style_sheet, "collapsable_frame"),
        ):
            with ui.VStack(spacing=5):
                # ...existing KPI metrics code...

                # Analytics actions
                with ui.HStack(spacing=5, height=30):
                    ui.Button(
                        "Detailed Analytics",
                        clicked_fn=self._show_analytics_dashboard,
                        style=get_style(self._style_sheet, "button"),
                    )

                    ui.Button(
                        "Generate Report",
                        clicked_fn=self._generate_analytics_report,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

    def _build_safety_overview(self):
        """Build safety overview panel"""
        with ui.CollapsableFrame(
            "Safety Overview",
            height=0,
            collapsed=True,
            style=get_style(self._style_sheet, "collapsable_frame"),
        ):
            with ui.VStack(spacing=5):
                # Safety metrics
                safety_data = self.safety_manager.get_safety_dashboard_data()
                overview = safety_data.get("overview", {})

                with ui.HStack(spacing=10, height=60):
                    # Compliance rate
                    with ui.VStack():
                        compliance_rate = overview.get("compliance_rate", 100)
                        color = (
                            "status_good"
                            if compliance_rate >= 95
                            else (
                                "status_warning"
                                if compliance_rate >= 85
                                else "status_error"
                            )
                        )
                        ui.Label(
                            f"{compliance_rate:.1f}%",
                            style=get_style(self._style_sheet, color),
                        )
                        ui.Label(
                            "Compliance",
                            style=get_style(self._style_sheet, "metric_label"),
                        )

                    ui.Separator(
                        width=2, style=get_style(self._style_sheet, "separator")
                    )

                    # Active violations
                    with ui.VStack():
                        violations = overview.get("active_violations", 0)
                        color = "status_good" if violations == 0 else "status_error"
                        ui.Label(
                            f"{violations}", style=get_style(self._style_sheet, color)
                        )
                        ui.Label(
                            "Violations",
                            style=get_style(self._style_sheet, "metric_label"),
                        )

                    ui.Separator(
                        width=2, style=get_style(self._style_sheet, "separator")
                    )

                    # Active alerts
                    with ui.VStack():
                        alerts = overview.get("active_alerts", 0)
                        color = "status_good" if alerts == 0 else "status_warning"
                        ui.Label(f"{alerts}", style=get_style(self._style_sheet, color))
                        ui.Label(
                            "Alerts", style=get_style(self._style_sheet, "metric_label")
                        )

                # Safety actions
                with ui.HStack(spacing=5, height=30):
                    ui.Button(
                        "Safety Dashboard",
                        click_fn=self._show_safety_dashboard,
                        style=get_style(self._style_sheet, "button_warning"),
                    )
                    ui.Button(
                        "Incident Report",
                        click_fn=self._create_incident_report,
                        style=get_style(self._style_sheet, "button_secondary"),
                    )

    def _build_sync_section(self):
        """Build the Isaac Sim synchronization section"""
        try:
            if self.sync_controller and self.sync_controller.ui_built:
                # UI already built
                return
            
            if not self.sync_controller:
                # Create controller if it doesn't exist
                self.sync_controller = SyncUIController(
                    self.ai_agent_manager, 
                    self._style_sheet
                )
            
            # Build the sync UI
            self.sync_controller.build_sync_ui()
            
        except Exception as e:
            carb.log_error(f"Employee Management: Failed to build sync section: {str(e)}")
            
            # Fallback: show a simple message
            with ui.CollapsableFrame(
                "Isaac Sim Synchronization",
                height=0,
                collapsed=True,
                style=get_style(self._style_sheet, "collapsable_frame"),
            ):
                ui.Label(
                    f"Sync system unavailable: {str(e)}",
                    style=get_style(self._style_sheet, "status_error"),
                )

    def _show_sync_config(self):
        """Show sync configuration dialog"""
        carb.log_info("Employee Management: Opening sync configuration")
        # This could open a more detailed configuration window if needed

    # Action handlers
    def _add_employee_dialog(self):
        """Show add employee dialog"""
        carb.log_info("Employee Management: Opening add employee dialog")

    def _start_tracking(self):
        """Start motion tracking"""
        try:
            success = self.motion_capture_manager.start_tracking()
            if success:
                carb.log_info("Employee Management: Tracking started")
            else:
                carb.log_error("Employee Management: Failed to start tracking")
        except Exception as e:
            carb.log_error(f"Employee Management: Error starting tracking: {str(e)}")

    def _emergency_stop(self):
        """Emergency stop all systems"""
        try:
            self.motion_capture_manager.stop_tracking()
            carb.log_warn("Employee Management: Emergency stop activated")
        except Exception as e:
            carb.log_error(
                f"Employee Management: Error during emergency stop: {str(e)}"
            )

    def _export_data(self):
        """Export analytics data"""
        try:
            data = self.analytics_manager.export_analytics_data()
            if data:
                carb.log_info("Employee Management: Data exported successfully")
            else:
                carb.log_error("Employee Management: Failed to export data")
        except Exception as e:
            carb.log_error(f"Employee Management: Error exporting data: {str(e)}")

    def _add_employee(self):
        """Add new employee"""
        try:
            employee_id = self._employee_id_field.model.get_value_as_string()
            if employee_id:
                success = self.motion_capture_manager.add_employee(employee_id)
                if success:
                    carb.log_info(f"Employee Management: Added employee {employee_id}")
                else:
                    carb.log_error(
                        f"Employee Management: Failed to add employee {employee_id}"
                    )
        except Exception as e:
            carb.log_error(f"Employee Management: Error adding employee: {str(e)}")

    def _remove_employee(self):
        """Remove employee"""
        try:
            employee_id = self._employee_id_field.model.get_value_as_string()
            if employee_id:
                success = self.motion_capture_manager.remove_employee(employee_id)
                if success:
                    carb.log_info(
                        f"Employee Management: Removed employee {employee_id}"
                    )
                else:
                    carb.log_error(
                        f"Employee Management: Failed to remove employee {employee_id}"
                    )
        except Exception as e:
            carb.log_error(f"Employee Management: Error removing employee: {str(e)}")

    def _configure_camera(self):
        """Configure camera mapping"""
        try:
            camera_id = self._camera_id_field.model.get_value_as_string()
            if camera_id:
                # Default camera configuration
                mapping_config = {
                    "world_origin_x": 0.0,
                    "world_origin_y": 0.0,
                    "scale_x": 0.01,  # Convert from pixels to meters
                    "scale_y": 0.01,
                    "offset_x": 0.0,
                    "offset_y": 0.0,
                    "ground_height": 0.0,
                    "rotation": 0.0,
                }
                success = self.motion_capture_manager.configure_camera_mapping(
                    camera_id, mapping_config
                )
                if success:
                    carb.log_info(f"Employee Management: Configured camera {camera_id}")
                else:
                    carb.log_error(
                        f"Employee Management: Failed to configure camera {camera_id}"
                    )
        except Exception as e:
            carb.log_error(f"Employee Management: Error configuring camera: {str(e)}")

    def _show_ai_config_dialog(self):
        """Show AI configuration dialog"""
        carb.log_info("Employee Management: Opening AI configuration")

    def _show_motion_capture_setup(self):
        """Show motion capture setup"""
        carb.log_info("Employee Management: Opening motion capture setup")

    def _show_analytics_dashboard(self):
        """Show detailed analytics dashboard"""
        carb.log_info("Employee Management: Opening analytics dashboard")

    def _show_safety_dashboard(self):
        """Show safety monitoring dashboard"""
        carb.log_info("Employee Management: Opening safety dashboard")

    def _generate_analytics_report(self):
        """Generate analytics report"""
        carb.log_info("Employee Management: Generating analytics report")

    def _create_incident_report(self):
        """Create incident report"""
        carb.log_info("Employee Management: Creating incident report")

    def _show_calibration_wizard(self):
        """Show camera calibration wizard"""
        self.calibration_manager.start_calibration_wizard()
        # Update status when calibration is completed
        if len(self.calibration_manager.get_calibrated_cameras()) > 0:
            self.system_status["camera_calibration"] = True

    def destroy(self):
        """Clean up resources"""
        try:
            # Shutdown systems
            asyncio.ensure_future(self._shutdown_systems())
            super().destroy()
        except Exception as e:
            carb.log_error(f"Employee Management: Error during shutdown: {str(e)}")

    async def _shutdown_systems(self):
        """Shutdown all systems"""
        try:
            # Shutdown sync controller first
            if self.sync_controller:
                self.sync_controller.shutdown()
            
            await self.ai_agent_manager.shutdown()
            self.motion_capture_manager.stop_tracking()
            carb.log_info("Employee Management: Systems shutdown complete")
        except Exception as e:
            carb.log_error(
                f"Employee Management: Error during systems shutdown: {str(e)}"
            )
