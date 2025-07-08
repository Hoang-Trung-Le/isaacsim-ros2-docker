"""
Isaac Sim Synchronization Manager

Handles real-time synchronization of employee positions from the warehouse agent
to Isaac Sim avatar positions with proper matrix4d transforms.
"""

import omni.usd
import carb
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from pxr import Usd, UsdGeom, Gf
from .global_variables import MOTION_UPDATE_INTERVAL


class IsaacSimSyncManager:
    """
    Manages synchronization between warehouse employee agent and Isaac Sim avatars
    Handles continuous position updates with proper matrix4d transforms
    """

    def __init__(self, ai_agent_manager):
        self.ai_agent_manager = ai_agent_manager
        self._context = omni.usd.get_context()
        self._stage = None
        
        # Sync configuration
        self.sync_active = False
        self.update_interval = 2.0  # Update every 2 seconds
        self.sync_task = None
        
        # Employee ID mapping (warehouse agent -> Isaac Sim)
        self.employee_mapping = {
            "EMP001": "/World/Worker_01",
            "EMP002": "/World/Worker_02", 
            "EMP003": "/World/Worker_03",
            "EMP004": "/World/Worker_04",
            "EMP005": "/World/Worker_05"
        }
        
        # Track last known positions to detect changes
        self.last_positions = {}
        
        # Transform configuration
        self.transform_config = {
            "scale_factor": 1.0,
            "height_offset": 0.0,  # Z offset for avatars (if needed)
            "coordinate_system": "right_handed"
        }
        
        carb.log_info("Isaac Sim Sync Manager: Initialized")

    async def initialize_sync_system(self) -> bool:
        """Initialize the synchronization system"""
        try:
            self._stage = self._context.get_stage()
            if not self._stage:
                carb.log_error("Isaac Sim Sync: No USD stage available")
                return False

            # Verify that all worker prims exist
            missing_workers = []
            for emp_id, worker_path in self.employee_mapping.items():
                worker_prim = self._stage.GetPrimAtPath(worker_path)
                if not worker_prim.IsValid():
                    missing_workers.append(worker_path)
                    carb.log_warn(f"Isaac Sim Sync: Worker not found at {worker_path}")

            if missing_workers:
                carb.log_error(f"Isaac Sim Sync: Missing workers: {missing_workers}")
                return False

            carb.log_info("Isaac Sim Sync: All workers verified, system ready")
            return True
            
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Failed to initialize: {str(e)}")
            return False

    def start_continuous_sync(self) -> bool:
        try:
            if self.sync_active:
                carb.log_warn("Isaac Sim Sync: Already active")
                return True

            if not self.ai_agent_manager.connected:
                carb.log_error("Isaac Sim Sync: AI Agent Manager not connected")
                return False

            self.sync_active = True

            try:
                loop = asyncio.get_running_loop()
                self.sync_task = loop.create_task(self._sync_loop())
            except RuntimeError:
                # No running event loop, so schedule it with ensure_future (may still fail if no loop)
                self.sync_task = asyncio.ensure_future(self._sync_loop())

            carb.log_info("Isaac Sim Sync: Started continuous synchronization")
            return True

        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Failed to start sync: {str(e)}")
            return False

    def stop_continuous_sync(self):
        """Stop continuous synchronization"""
        try:
            self.sync_active = False
            if self.sync_task:
                self.sync_task.cancel()
                self.sync_task = None
            carb.log_info("Isaac Sim Sync: Stopped continuous synchronization")
            
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Error stopping sync: {str(e)}")

    async def _sync_loop(self):
        """Main synchronization loop"""
        carb.log_info("Isaac Sim Sync: Starting sync loop")
        
        while self.sync_active:
            try:
                # Get latest employee positions from warehouse agent
                positions_data = await self.ai_agent_manager.get_warehouse_employee_positions()
                
                if positions_data and positions_data.get("status") == "success":
                    await self._update_avatar_positions(positions_data.get("employees", []))
                else:
                    carb.log_warn("Isaac Sim Sync: Failed to get employee positions")
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
                
            except asyncio.CancelledError:
                carb.log_info("Isaac Sim Sync: Sync loop cancelled")
                break
            except Exception as e:
                carb.log_error(f"Isaac Sim Sync: Error in sync loop: {str(e)}")
                await asyncio.sleep(self.update_interval)  # Continue despite errors

    async def _update_avatar_positions(self, employees: List[Dict[str, Any]]):
        """Update avatar positions based on employee data"""
        try:
            updated_count = 0
            
            for employee in employees:
                emp_id = employee.get("id", "")
                position = employee.get("position", [0, 0, 0])
                
                if emp_id in self.employee_mapping:
                    # Check if position has changed significantly
                    if self._position_changed(emp_id, position):
                        success = await self._update_single_avatar(emp_id, position)
                        if success:
                            updated_count += 1
                            self.last_positions[emp_id] = position.copy()
            
            if updated_count > 0:
                carb.log_info(f"Isaac Sim Sync: Updated {updated_count} avatars")
                
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Error updating avatar positions: {str(e)}")

    def _position_changed(self, emp_id: str, new_position: List[float], threshold: float = 0.1) -> bool:
        """Check if position has changed significantly"""
        if emp_id not in self.last_positions:
            return True
        
        last_pos = self.last_positions[emp_id]
        distance = sum((new_position[i] - last_pos[i]) ** 2 for i in range(3)) ** 0.5
        return distance > threshold

    async def _update_single_avatar(self, emp_id: str, position: List[float]) -> bool:
        """Update a single avatar's position using matrix4d transform"""
        try:
            worker_path = self.employee_mapping[emp_id]
            worker_prim = self._stage.GetPrimAtPath(worker_path)
            
            if not worker_prim.IsValid():
                carb.log_error(f"Isaac Sim Sync: Worker prim not valid: {worker_path}")
                return False

            # Get the xformable
            xformable = UsdGeom.Xformable(worker_prim)
            
            # Apply transform configuration
            x, y, z = position
            x *= self.transform_config["scale_factor"]
            y *= self.transform_config["scale_factor"]
            z += self.transform_config["height_offset"]
            
            # Create transformation matrix
            # Isaac Sim uses right-handed coordinate system by default
            transform_matrix = Gf.Matrix4d(
                1.0, 0.0, 0.0, 0.0,  # Row 1: X axis and translation
                0.0, 1.0, 0.0, 0.0,  # Row 2: Y axis and translation
                0.0, 0.0, 1.0, 0.0,  # Row 3: Z axis and translation
                x,   y,   z,   1.0   # Row 4: Translation and homogeneous coordinate
            )
            
            # Get or create the transform operation
            transform_ops = xformable.GetOrderedXformOps()
            transform_op = None
            
            # Look for existing xformOp:transform
            for op in transform_ops:
                if op.GetOpName() == "xformOp:transform":
                    transform_op = op
                    break
            
            # If no transform op exists, create one
            if not transform_op:
                transform_op = xformable.AddTransformOp()
            
            # Set the matrix
            transform_op.Set(transform_matrix)
            
            carb.log_error(f"Isaac Sim Sync: Updated {emp_id} -> {worker_path} to position {position}")
            return True
            
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Failed to update {emp_id}: {str(e)}")
            return False

    async def manual_sync_once(self) -> Dict[str, Any]:
        """Perform a single manual synchronization"""
        try:
            carb.log_info("Isaac Sim Sync: Performing manual sync")
            
            # Get employee positions
            positions_data = await self.ai_agent_manager.get_warehouse_employee_positions()
            
            if not positions_data or positions_data.get("status") != "success":
                return {
                    "success": False,
                    "message": "Failed to get employee positions",
                    "data": positions_data
                }
            
            employees = positions_data.get("employees", [])
            
            # Update avatars
            await self._update_avatar_positions(employees)
            
            # Prepare response
            updated_employees = []
            for employee in employees:
                emp_id = employee.get("id", "")
                if emp_id in self.employee_mapping:
                    updated_employees.append({
                        "employee_id": emp_id,
                        "worker_path": self.employee_mapping[emp_id],
                        "position": employee.get("position", [0, 0, 0]),
                        "zone": employee.get("zone", "unknown")
                    })
            
            return {
                "success": True,
                "message": f"Successfully synced {len(updated_employees)} avatars",
                "timestamp": time.time(),
                "updated_employees": updated_employees,
                "source_data": positions_data
            }
            
        except Exception as e:
            error_msg = f"Manual sync failed: {str(e)}"
            carb.log_error(f"Isaac Sim Sync: {error_msg}")
            return {
                "success": False,
                "message": error_msg
            }

    def configure_sync_settings(self, update_interval: float = None, 
                               employee_mapping: Dict[str, str] = None,
                               transform_config: Dict[str, Any] = None):
        """Configure synchronization settings"""
        try:
            if update_interval is not None:
                self.update_interval = max(0.5, update_interval)  # Minimum 0.5 seconds
                carb.log_info(f"Isaac Sim Sync: Update interval set to {self.update_interval}s")
            
            if employee_mapping is not None:
                self.employee_mapping.update(employee_mapping)
                carb.log_info("Isaac Sim Sync: Employee mapping updated")
            
            if transform_config is not None:
                self.transform_config.update(transform_config)
                carb.log_info("Isaac Sim Sync: Transform configuration updated")
                
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Failed to configure settings: {str(e)}")

    def get_sync_status(self) -> Dict[str, Any]:
        """Get current synchronization status"""
        return {
            "sync_active": self.sync_active,
            "update_interval": self.update_interval,
            "employee_mapping": self.employee_mapping,
            "last_positions": self.last_positions,
            "transform_config": self.transform_config,
            "ai_agent_connected": self.ai_agent_manager.connected if self.ai_agent_manager else False
        }

    def validate_worker_prims(self) -> Dict[str, bool]:
        """Validate that all worker prims exist in the stage"""
        validation_results = {}
        
        try:
            if not self._stage:
                self._stage = self._context.get_stage()
            
            for emp_id, worker_path in self.employee_mapping.items():
                worker_prim = self._stage.GetPrimAtPath(worker_path)
                validation_results[worker_path] = worker_prim.IsValid()
                
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Error validating worker prims: {str(e)}")
        
        return validation_results

    def shutdown(self):
        """Shutdown the sync manager"""
        try:
            self.stop_continuous_sync()
            carb.log_info("Isaac Sim Sync: Shutdown complete")
        except Exception as e:
            carb.log_error(f"Isaac Sim Sync: Error during shutdown: {str(e)}") 