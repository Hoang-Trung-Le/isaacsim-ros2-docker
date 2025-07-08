"""
Sync UI Controller

Manages UI components and interactions for Isaac Sim synchronization functionality
"""

import omni.ui as ui
import carb
import asyncio
import json
from typing import Dict, Any, Optional
from .isaac_sim_sync_manager import IsaacSimSyncManager
from .style import get_style


class SyncUIController:
    """
    Controls UI elements and interactions for Isaac Sim synchronization
    """

    def __init__(self, ai_agent_manager, style_sheet=None):
        self.ai_agent_manager = ai_agent_manager
        self.style_sheet = style_sheet
        
        # Initialize sync manager
        self.sync_manager = IsaacSimSyncManager(ai_agent_manager)
        
        # UI elements
        self.sync_status_label = None
        self.sync_toggle_button = None
        self.update_interval_field = None
        self.response_field = None
        
        # Status tracking
        self.is_initialized = False
        self.ui_built = False
        
        carb.log_info("Sync UI Controller: Initialized")

    async def initialize_async(self) -> bool:
        """Initialize the sync system asynchronously"""
        try:
            success = await self.sync_manager.initialize_sync_system()
            self.is_initialized = success
            
            if success:
                carb.log_info("Sync UI Controller: Sync system initialized successfully")
                self._update_ui_status()
            else:
                carb.log_error("Sync UI Controller: Failed to initialize sync system")
            
            return success
            
        except Exception as e:
            carb.log_error(f"Sync UI Controller: Initialization error: {str(e)}")
            return False

    def build_sync_ui(self, parent_container=None) -> bool:
        """Build the sync UI components"""
        try:
            # Build UI in current context if no parent provided
            with ui.CollapsableFrame(
                "Isaac Sim Synchronization",
                height=0,
                collapsed=False,
                style=get_style(self.style_sheet, "collapsable_frame"),
            ):
                with ui.VStack(spacing=5):
                    # Status section
                    self._build_status_section()
                    ui.Separator(style=get_style(self.style_sheet, "separator"))
                    
                    # Control section
                    self._build_control_section()
                    ui.Separator(style=get_style(self.style_sheet, "separator"))
                    
                    # Configuration section
                    self._build_configuration_section()
                    ui.Separator(style=get_style(self.style_sheet, "separator"))
                    
                    # Response section
                    self._build_response_section()
            
            self.ui_built = True
            carb.log_info("Sync UI Controller: UI built successfully")
            return True
            
        except Exception as e:
            carb.log_error(f"Sync UI Controller: Failed to build UI: {str(e)}")
            return False

    def _build_status_section(self):
        """Build the status display section"""
        ui.Label(
            "Synchronization Status:",
            style=get_style(self.style_sheet, "label"),
        )
        
        with ui.HStack(height=25):
            ui.Label(
                "Status:",
                width=80,
                style=get_style(self.style_sheet, "label"),
            )
            self.sync_status_label = ui.Label(
                "Initializing...",
                style=get_style(self.style_sheet, "status_warning"),
            )
            ui.Spacer()

    def _build_control_section(self):
        """Build the control buttons section"""
        ui.Label(
            "Sync Controls:",
            style=get_style(self.style_sheet, "label"),
        )
        
        with ui.HStack(spacing=5, height=30):
            # Manual sync button
            ui.Button(
                "Manual Sync",
                width=100,
                clicked_fn=self._manual_sync,
                style=get_style(self.style_sheet, "button"),
            )
            
            # Toggle continuous sync button
            self.sync_toggle_button = ui.Button(
                "Start Auto Sync",
                width=120,
                clicked_fn=self._toggle_continuous_sync,
                style=get_style(self.style_sheet, "button_success"),
            )
            
            # Validate workers button
            ui.Button(
                "Validate Workers",
                width=120,
                clicked_fn=self._validate_workers,
                style=get_style(self.style_sheet, "button_secondary"),
            )
            
            ui.Spacer()

    def _build_configuration_section(self):
        """Build the configuration section"""
        ui.Label(
            "Sync Configuration:",
            style=get_style(self.style_sheet, "label"),
        )
        
        with ui.HStack(spacing=5, height=30):
            ui.Label(
                "Update Interval (s):",
                width=120,
                style=get_style(self.style_sheet, "label"),
            )
            
            self.update_interval_field = ui.FloatField(
                width=80,
                style=get_style(self.style_sheet, "text_field"),
            )
            self.update_interval_field.model.set_value(2.0)
            
            ui.Button(
                "Apply",
                width=60,
                clicked_fn=self._apply_configuration,
                style=get_style(self.style_sheet, "button_secondary"),
            )
            
            ui.Spacer()

    def _build_response_section(self):
        """Build the response display section"""
        ui.Label(
            "Sync Response:",
            style=get_style(self.style_sheet, "label"),
        )
        
        self.response_field = ui.StringField(
            multiline=True,
            height=200,
            style=get_style(self.style_sheet, "text_field"),
        )
        self.response_field.model.set_value("Ready for synchronization operations...")

    def _manual_sync(self):
        """Handle manual sync button click"""
        carb.log_info("Sync UI Controller: Manual sync requested")
        asyncio.ensure_future(self._async_manual_sync())

    async def _async_manual_sync(self):
        """Perform manual sync asynchronously"""
        try:
            if not self.is_initialized:
                await self.initialize_async()
            
            if not self.is_initialized:
                self._update_response("Error: Sync system not initialized")
                return
            
            # Perform manual sync
            result = await self.sync_manager.manual_sync_once()
            
            # Update response display
            response_text = json.dumps(result, indent=2)
            self._update_response(response_text)
            
            # Update status
            self._update_ui_status()
            
            if result.get("success", False):
                carb.log_info("Sync UI Controller: Manual sync completed successfully")
            else:
                carb.log_error("Sync UI Controller: Manual sync failed")
                
        except Exception as e:
            error_msg = f"Manual sync error: {str(e)}"
            self._update_response(error_msg)
            carb.log_error(f"Sync UI Controller: {error_msg}")

    def _toggle_continuous_sync(self):
        """Toggle continuous synchronization"""
        try:
            if not self.is_initialized:
                asyncio.ensure_future(self._async_initialize_and_toggle())
                return
            
            if self.sync_manager.sync_active:
                self.sync_manager.stop_continuous_sync()
                self.sync_toggle_button.text = "Start Auto Sync"
                self.sync_toggle_button.style = get_style(self.style_sheet, "button_success")
                self._update_response("Continuous synchronization stopped")
            else:
                success = self.sync_manager.start_continuous_sync()
                if success:
                    self.sync_toggle_button.text = "Stop Auto Sync"
                    self.sync_toggle_button.style = get_style(self.style_sheet, "button_danger")
                    self._update_response("Continuous synchronization started")
                else:
                    self._update_response("Failed to start continuous synchronization")
            
            self._update_ui_status()
            
        except Exception as e:
            error_msg = f"Toggle sync error: {str(e)}"
            self._update_response(error_msg)
            carb.log_error(f"Sync UI Controller: {error_msg}")

    async def _async_initialize_and_toggle(self):
        """Initialize system and then toggle sync"""
        await self.initialize_async()
        self._toggle_continuous_sync()

    def _validate_workers(self):
        """Validate worker prims in the scene"""
        try:
            validation_results = self.sync_manager.validate_worker_prims()
            
            response = {
                "validation_results": validation_results,
                "timestamp": asyncio.get_event_loop().time(),
                "summary": {
                    "total_workers": len(validation_results),
                    "valid_workers": sum(validation_results.values()),
                    "invalid_workers": len(validation_results) - sum(validation_results.values())
                }
            }
            
            response_text = json.dumps(response, indent=2)
            self._update_response(response_text)
            
            if response["summary"]["invalid_workers"] > 0:
                carb.log_warn("Sync UI Controller: Some worker prims are invalid")
            else:
                carb.log_info("Sync UI Controller: All worker prims are valid")
                
        except Exception as e:
            error_msg = f"Worker validation error: {str(e)}"
            self._update_response(error_msg)
            carb.log_error(f"Sync UI Controller: {error_msg}")

    def _apply_configuration(self):
        """Apply configuration changes"""
        try:
            if self.update_interval_field:
                new_interval = self.update_interval_field.model.get_value_as_float()
                self.sync_manager.configure_sync_settings(update_interval=new_interval)
                
                response_msg = f"Configuration updated: Update interval set to {new_interval}s"
                self._update_response(response_msg)
                carb.log_info(f"Sync UI Controller: {response_msg}")
                
        except Exception as e:
            error_msg = f"Configuration error: {str(e)}"
            self._update_response(error_msg)
            carb.log_error(f"Sync UI Controller: {error_msg}")

    def _update_response(self, message: str):
        """Update the response field"""
        if self.response_field:
            self.response_field.model.set_value(message)

    def _update_ui_status(self):
        """Update UI status indicators"""
        try:
            if not self.sync_status_label:
                return
            
            if not self.is_initialized:
                self.sync_status_label.text = "Not Initialized"
                self.sync_status_label.style = get_style(self.style_sheet, "status_error")
            elif self.sync_manager.sync_active:
                self.sync_status_label.text = "Auto Sync Active"
                self.sync_status_label.style = get_style(self.style_sheet, "status_good")
            else:
                self.sync_status_label.text = "Ready"
                self.sync_status_label.style = get_style(self.style_sheet, "status_warning")
                
        except Exception as e:
            carb.log_error(f"Sync UI Controller: Error updating UI status: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """Get current controller status"""
        sync_status = self.sync_manager.get_sync_status() if self.sync_manager else {}
        
        return {
            "ui_built": self.ui_built,
            "is_initialized": self.is_initialized,
            "sync_manager_status": sync_status
        }

    def shutdown(self):
        """Shutdown the controller"""
        try:
            if self.sync_manager:
                self.sync_manager.shutdown()
            carb.log_info("Sync UI Controller: Shutdown complete")
        except Exception as e:
            carb.log_error(f"Sync UI Controller: Error during shutdown: {str(e)}") 