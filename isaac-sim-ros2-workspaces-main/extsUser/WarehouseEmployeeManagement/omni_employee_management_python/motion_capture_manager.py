import omni.usd
import carb
import asyncio
import json
from pxr import Usd, UsdGeom, Gf, UsdSkel
from typing import Dict, List, Tuple, Optional, Any
from .global_variables import (
    MOTION_UPDATE_INTERVAL, 
    DEFAULT_AVATAR_SCALE,
    DEFAULT_AVATAR_COLOR,
    SAFETY_VIOLATION_COLOR,
    COORDINATE_SYSTEM
)


class MotionCaptureManager:
    """
    Manages real-time human motion capture with digital twin synchronization
    Receives bounding box coordinates from real-world cameras and updates virtual avatars
    """

    def __init__(self):
        self._context = omni.usd.get_context()
        self._stage = None
        self.employees = {}  # employee_id -> avatar data
        self.camera_mappings = {}  # camera_id -> mapping configuration
        self.active_tracking = False
        self.update_timer = None
        
        # Avatar management
        self.avatar_template_path = "/World/Avatars/EmployeeTemplate"
        self.avatars_root_path = "/World/Avatars"
        
        # Coordinate transformation
        self.coordinate_transform = self._init_coordinate_transform()

    def _init_coordinate_transform(self) -> Dict[str, Any]:
        """Initialize coordinate transformation settings"""
        return {
            "scale_factor": 1.0,
            "offset": (0.0, 0.0, 0.0),
            "rotation": (0.0, 0.0, 0.0),
            "coordinate_system": COORDINATE_SYSTEM
        }

    async def initialize_avatars_system(self) -> bool:
        """Initialize the avatar system in the USD stage"""
        try:
            self._stage = self._context.get_stage()
            if not self._stage:
                carb.log_error("Motion Capture: No USD stage available")
                return False

            # Create avatars root prim if it doesn't exist
            avatars_root = self._stage.GetPrimAtPath(self.avatars_root_path)
            if not avatars_root:
                avatars_root = UsdGeom.Xform.Define(self._stage, self.avatars_root_path)
                carb.log_info(f"Motion Capture: Created avatars root at {self.avatars_root_path}")

            # Create or load avatar template
            await self._setup_avatar_template()
            
            carb.log_info("Motion Capture: Avatar system initialized")
            return True
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to initialize avatar system: {str(e)}")
            return False

    async def _setup_avatar_template(self):
        """Setup the base avatar template"""
        try:
            template_prim = self._stage.GetPrimAtPath(self.avatar_template_path)
            if not template_prim:
                # Create a simple capsule as avatar template
                template_prim = UsdGeom.Capsule.Define(self._stage, self.avatar_template_path)
                capsule = UsdGeom.Capsule(template_prim)
                capsule.CreateHeightAttr(1.8)  # Average human height
                capsule.CreateRadiusAttr(0.3)   # Average human width
                
                # Set default transform
                xform = UsdGeom.Xformable(template_prim)
                xform.AddTranslateOp().Set((0, 0, 0.9))  # Half height above ground
                
                # Add color attribute
                capsule.CreateDisplayColorAttr([DEFAULT_AVATAR_COLOR])
                
                # Hide template (make it invisible)
                template_prim.SetActive(False)
                
                carb.log_info("Motion Capture: Created avatar template")
                
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to setup avatar template: {str(e)}")

    def add_employee(self, employee_id: str, initial_position: Tuple[float, float, float] = (0, 0, 0)) -> bool:
        """Add a new employee to tracking"""
        try:
            if employee_id in self.employees:
                carb.log_warn(f"Motion Capture: Employee {employee_id} already exists")
                return True

            # Create avatar for employee
            avatar_path = f"{self.avatars_root_path}/Employee_{employee_id}"
            avatar_prim = self._stage.GetPrimAtPath(avatar_path)
            
            if not avatar_prim:
                # Reference the template to create new avatar
                avatar_prim = UsdGeom.Capsule.Define(self._stage, avatar_path)
                capsule = UsdGeom.Capsule(avatar_prim)
                capsule.CreateHeightAttr(1.8)
                capsule.CreateRadiusAttr(0.3)
                capsule.CreateDisplayColorAttr([DEFAULT_AVATAR_COLOR])
                
                # Set initial position
                xform = UsdGeom.Xformable(avatar_prim)
                translate_op = xform.AddTranslateOp()
                translate_op.Set((initial_position[0], initial_position[1], initial_position[2] + 0.9))
                
                # Make it active/visible
                avatar_prim.SetActive(True)

            # Store employee data
            self.employees[employee_id] = {
                "avatar_path": avatar_path,
                "current_position": initial_position,
                "last_update": 0,
                "status": "active",
                "safety_status": "compliant",
                "avatar_prim": avatar_prim
            }
            
            carb.log_info(f"Motion Capture: Added employee {employee_id}")
            return True
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to add employee {employee_id}: {str(e)}")
            return False

    def remove_employee(self, employee_id: str) -> bool:
        """Remove an employee from tracking"""
        try:
            if employee_id not in self.employees:
                carb.log_warn(f"Motion Capture: Employee {employee_id} not found")
                return False

            # Remove avatar from stage
            avatar_path = self.employees[employee_id]["avatar_path"]
            avatar_prim = self._stage.GetPrimAtPath(avatar_path)
            if avatar_prim:
                self._stage.RemovePrim(avatar_path)

            # Remove from tracking
            del self.employees[employee_id]
            
            carb.log_info(f"Motion Capture: Removed employee {employee_id}")
            return True
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to remove employee {employee_id}: {str(e)}")
            return False

    def update_employee_position(self, employee_id: str, camera_id: str, bbox_data: Dict[str, Any]) -> bool:
        """
        Update employee position from camera bounding box data
        
        Args:
            employee_id: Unique identifier for employee
            camera_id: Camera that detected the employee
            bbox_data: Bounding box data with format:
                {
                    "x": center_x,
                    "y": center_y,
                    "width": bbox_width,
                    "height": bbox_height,
                    "confidence": detection_confidence
                }
        """
        try:
            if employee_id not in self.employees:
                # Auto-add employee if not exists
                self.add_employee(employee_id)

            # Transform camera coordinates to virtual world coordinates
            virtual_position = self._transform_camera_to_virtual(camera_id, bbox_data)
            
            if virtual_position is None:
                carb.log_warn(f"Motion Capture: Failed to transform coordinates for camera {camera_id}")
                return False

            # Update avatar position
            employee_data = self.employees[employee_id]
            avatar_prim = employee_data["avatar_prim"]
            
            if avatar_prim:
                xform = UsdGeom.Xformable(avatar_prim)
                translate_ops = xform.GetOrderedXformOps()
                
                if translate_ops:
                    # Update existing transform
                    translate_ops[0].Set((virtual_position[0], virtual_position[1], virtual_position[2] + 0.9))
                else:
                    # Create new transform
                    translate_op = xform.AddTranslateOp()
                    translate_op.Set((virtual_position[0], virtual_position[1], virtual_position[2] + 0.9))

                # Update employee data
                employee_data["current_position"] = virtual_position
                employee_data["last_update"] = carb.get_frame_count()
                
                return True
                
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to update employee {employee_id} position: {str(e)}")
            return False

    def _transform_camera_to_virtual(self, camera_id: str, bbox_data: Dict[str, Any]) -> Optional[Tuple[float, float, float]]:
        """Transform camera coordinates to virtual world coordinates"""
        try:
            if camera_id not in self.camera_mappings:
                carb.log_warn(f"Motion Capture: Camera {camera_id} not configured")
                return None

            mapping = self.camera_mappings[camera_id]
            
            # Extract bounding box center
            center_x = bbox_data.get("x", 0)
            center_y = bbox_data.get("y", 0)
            
            # Transform to virtual coordinates using camera mapping
            # This is a simplified transformation - in production, you'd use proper camera calibration
            virtual_x = (center_x - mapping["offset_x"]) * mapping["scale_x"] + mapping["world_origin_x"]
            virtual_y = (center_y - mapping["offset_y"]) * mapping["scale_y"] + mapping["world_origin_y"]
            virtual_z = mapping.get("ground_height", 0.0)
            
            return (virtual_x, virtual_y, virtual_z)
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Coordinate transformation failed: {str(e)}")
            return None

    def configure_camera_mapping(self, camera_id: str, mapping_config: Dict[str, Any]) -> bool:
        """
        Configure camera to virtual world coordinate mapping
        
        Args:
            camera_id: Unique camera identifier
            mapping_config: Mapping configuration with format:
                {
                    "world_origin_x": 0.0,
                    "world_origin_y": 0.0,
                    "scale_x": 1.0,
                    "scale_y": 1.0,
                    "offset_x": 0.0,
                    "offset_y": 0.0,
                    "ground_height": 0.0,
                    "rotation": 0.0
                }
        """
        try:
            required_fields = ["world_origin_x", "world_origin_y", "scale_x", "scale_y"]
            for field in required_fields:
                if field not in mapping_config:
                    carb.log_error(f"Motion Capture: Missing required field {field} in camera mapping")
                    return False

            self.camera_mappings[camera_id] = mapping_config
            carb.log_info(f"Motion Capture: Configured camera {camera_id} mapping")
            return True
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to configure camera mapping: {str(e)}")
            return False

    def set_employee_safety_status(self, employee_id: str, safety_status: str):
        """Update employee safety status and avatar appearance"""
        try:
            if employee_id not in self.employees:
                return

            employee_data = self.employees[employee_id]
            employee_data["safety_status"] = safety_status
            
            # Update avatar color based on safety status
            avatar_prim = employee_data["avatar_prim"]
            if avatar_prim:
                capsule = UsdGeom.Capsule(avatar_prim)
                if safety_status == "violation":
                    capsule.CreateDisplayColorAttr([SAFETY_VIOLATION_COLOR])
                else:
                    capsule.CreateDisplayColorAttr([DEFAULT_AVATAR_COLOR])
                    
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to update safety status: {str(e)}")

    def start_tracking(self) -> bool:
        """Start motion capture tracking"""
        try:
            if self.active_tracking:
                carb.log_warn("Motion Capture: Tracking already active")
                return True

            self.active_tracking = True
            carb.log_info("Motion Capture: Tracking started")
            return True
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to start tracking: {str(e)}")
            return False

    def stop_tracking(self):
        """Stop motion capture tracking"""
        try:
            self.active_tracking = False
            carb.log_info("Motion Capture: Tracking stopped")
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to stop tracking: {str(e)}")

    def get_tracking_status(self) -> Dict[str, Any]:
        """Get current tracking status"""
        return {
            "active": self.active_tracking,
            "employee_count": len(self.employees),
            "camera_count": len(self.camera_mappings),
            "employees": {emp_id: {
                "position": data["current_position"],
                "status": data["status"],
                "safety_status": data["safety_status"],
                "last_update": data["last_update"]
            } for emp_id, data in self.employees.items()}
        }

    def get_employee_list(self) -> List[str]:
        """Get list of tracked employee IDs"""
        return list(self.employees.keys())

    def clear_all_employees(self):
        """Remove all employees from tracking"""
        try:
            employee_ids = list(self.employees.keys())
            for employee_id in employee_ids:
                self.remove_employee(employee_id)
            carb.log_info("Motion Capture: Cleared all employees")
            
        except Exception as e:
            carb.log_error(f"Motion Capture: Failed to clear employees: {str(e)}")
