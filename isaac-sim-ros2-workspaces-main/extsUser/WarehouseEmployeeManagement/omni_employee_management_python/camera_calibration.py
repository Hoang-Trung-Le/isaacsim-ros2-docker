"""
Camera Calibration Utilities for Employee Management Extension

This module provides utilities for calibrating cameras in the warehouse/factory
environment to ensure accurate coordinate transformation from camera space to
Isaac Sim world space.
"""

import omni.ext
import omni.ui as ui
import omni.usd
from pxr import Usd, UsdGeom, Gf
import asyncio
import carb
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os


class CameraCalibrationManager:
    """Handles camera calibration for accurate world coordinate mapping."""
    
    def __init__(self):
        self._calibration_data = {}
        self._calibration_points = []
        self._is_calibrating = False
        
    def start_calibration_wizard(self) -> None:
        """Start the interactive camera calibration wizard."""
        self._calibration_window = ui.Window(
            "Camera Calibration Wizard",
            width=400,
            height=600,
            flags=ui.WINDOW_FLAGS_NO_COLLAPSE
        )
        
        with self._calibration_window.frame:
            with ui.VStack(spacing=10):
                ui.Label("Camera Calibration Setup", style={"font_size": 18})
                ui.Separator()
                
                ui.Label("Follow these steps to calibrate your camera:")
                
                with ui.VStack(spacing=5):
                    ui.Label("1. Position known reference objects in the scene")
                    ui.Label("2. Mark corresponding points in camera view")
                    ui.Label("3. Record world coordinates for each point")
                    ui.Label("4. Generate transformation matrix")
                
                ui.Separator()
                
                # Camera selection
                ui.Label("Select Camera:")
                self._camera_combo = ui.ComboBox(0, "Camera_01", "Camera_02", "Camera_03")
                
                # Calibration points
                ui.Label("Calibration Points:")
                with ui.ScrollingFrame(height=200):
                    self._points_container = ui.VStack()
                    self._update_calibration_points_ui()
                
                # Controls
                with ui.HStack():
                    ui.Button("Add Point", clicked_fn=self._add_calibration_point)
                    ui.Button("Clear All", clicked_fn=self._clear_calibration_points)
                
                ui.Separator()
                
                with ui.HStack():
                    ui.Button("Start Calibration", clicked_fn=self._start_calibration)
                    ui.Button("Save Calibration", clicked_fn=self._save_calibration)
                    ui.Button("Load Calibration", clicked_fn=self._load_calibration)
    
    def _add_calibration_point(self) -> None:
        """Add a new calibration point."""
        point_data = {
            'id': len(self._calibration_points),
            'camera_x': 0.0,
            'camera_y': 0.0,
            'world_x': 0.0,
            'world_y': 0.0,
            'world_z': 0.0
        }
        self._calibration_points.append(point_data)
        self._update_calibration_points_ui()
    
    def _clear_calibration_points(self) -> None:
        """Clear all calibration points."""
        self._calibration_points.clear()
        self._update_calibration_points_ui()
    
    def _update_calibration_points_ui(self) -> None:
        """Update the calibration points UI."""
        if hasattr(self, '_points_container'):
            self._points_container.clear()
            
            with self._points_container:
                for i, point in enumerate(self._calibration_points):
                    with ui.CollapsibleFrame(f"Point {i+1}", collapsed=False):
                        with ui.VStack(spacing=5):
                            # Camera coordinates
                            ui.Label("Camera Coordinates (pixels):")
                            with ui.HStack():
                                ui.Label("X:", width=20)
                                ui.FloatDrag(
                                    model=ui.SimpleFloatModel(point['camera_x']),
                                    min=0, max=9999
                                )
                                ui.Label("Y:", width=20)
                                ui.FloatDrag(
                                    model=ui.SimpleFloatModel(point['camera_y']),
                                    min=0, max=9999
                                )
                            
                            # World coordinates
                            ui.Label("World Coordinates (meters):")
                            with ui.HStack():
                                ui.Label("X:", width=20)
                                ui.FloatDrag(
                                    model=ui.SimpleFloatModel(point['world_x']),
                                    min=-1000, max=1000
                                )
                            with ui.HStack():
                                ui.Label("Y:", width=20)
                                ui.FloatDrag(
                                    model=ui.SimpleFloatModel(point['world_y']),
                                    min=-1000, max=1000
                                )
                            with ui.HStack():
                                ui.Label("Z:", width=20)
                                ui.FloatDrag(
                                    model=ui.SimpleFloatModel(point['world_z']),
                                    min=-1000, max=1000
                                )
                            
                            ui.Button(
                                f"Remove Point {i+1}",
                                clicked_fn=lambda p=point: self._remove_point(p)
                            )
    
    def _remove_point(self, point: Dict) -> None:
        """Remove a calibration point."""
        if point in self._calibration_points:
            self._calibration_points.remove(point)
            self._update_calibration_points_ui()
    
    def _start_calibration(self) -> None:
        """Start the calibration process."""
        if len(self._calibration_points) < 4:
            carb.log_warn("Need at least 4 calibration points for accurate calibration")
            return
        
        try:
            # Calculate transformation matrix using collected points
            camera_points = np.array([[p['camera_x'], p['camera_y']] for p in self._calibration_points])
            world_points = np.array([[p['world_x'], p['world_y'], p['world_z']] for p in self._calibration_points])
            
            # Compute homography/transformation matrix
            transformation_matrix = self._calculate_transformation_matrix(camera_points, world_points)
            
            camera_name = f"Camera_{self._camera_combo.model.get_item_value_model().as_int:02d}"
            self._calibration_data[camera_name] = {
                'transformation_matrix': transformation_matrix.tolist(),
                'calibration_points': self._calibration_points.copy(),
                'timestamp': asyncio.get_event_loop().time()
            }
            
            carb.log_info(f"Calibration completed for {camera_name}")
            
        except Exception as e:
            carb.log_error(f"Calibration failed: {str(e)}")
    
    def _calculate_transformation_matrix(self, camera_points: np.ndarray, world_points: np.ndarray) -> np.ndarray:
        """Calculate transformation matrix from camera to world coordinates."""
        # For now, use a simplified perspective transformation
        # In a real implementation, you'd use more sophisticated camera calibration
        
        # Create homogeneous coordinates
        camera_homog = np.column_stack([camera_points, np.ones(len(camera_points))])
        
        # Solve for transformation matrix using least squares
        # This is a simplified version - real calibration would use proper camera matrix
        A = []
        b = []
        
        for i in range(len(camera_points)):
            x_cam, y_cam = camera_points[i]
            x_world, y_world, z_world = world_points[i]
            
            A.append([x_cam, y_cam, 1, 0, 0, 0])
            A.append([0, 0, 0, x_cam, y_cam, 1])
            b.append(x_world)
            b.append(y_world)
        
        A = np.array(A)
        b = np.array(b)
        
        # Solve using least squares
        transformation_params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        
        # Reshape into transformation matrix
        transform_matrix = np.array([
            [transformation_params[0], transformation_params[1], transformation_params[2]],
            [transformation_params[3], transformation_params[4], transformation_params[5]],
            [0, 0, 1]
        ])
        
        return transform_matrix
    
    def _save_calibration(self) -> None:
        """Save calibration data to file."""
        try:
            calibration_file = "/media/data/trunglh12/Projects/DigitalTwins/Omniverse/EmployeeManagement/data/camera_calibration.json"
            
            with open(calibration_file, 'w') as f:
                json.dump(self._calibration_data, f, indent=2)
            
            carb.log_info(f"Calibration data saved to {calibration_file}")
            
        except Exception as e:
            carb.log_error(f"Failed to save calibration: {str(e)}")
    
    def _load_calibration(self) -> None:
        """Load calibration data from file."""
        try:
            calibration_file = "/media/data/trunglh12/Projects/DigitalTwins/Omniverse/EmployeeManagement/data/camera_calibration.json"
            
            if os.path.exists(calibration_file):
                with open(calibration_file, 'r') as f:
                    self._calibration_data = json.load(f)
                
                carb.log_info(f"Calibration data loaded from {calibration_file}")
            else:
                carb.log_warn("No calibration file found")
                
        except Exception as e:
            carb.log_error(f"Failed to load calibration: {str(e)}")
    
    def transform_coordinates(self, camera_name: str, camera_x: float, camera_y: float) -> Tuple[float, float, float]:
        """Transform camera coordinates to world coordinates."""
        if camera_name not in self._calibration_data:
            carb.log_warn(f"No calibration data for camera {camera_name}")
            # Return default transformation as fallback
            return camera_x * 0.01, camera_y * 0.01, 0.0
        
        try:
            transformation_matrix = np.array(self._calibration_data[camera_name]['transformation_matrix'])
            
            # Apply transformation
            camera_coords = np.array([camera_x, camera_y, 1])
            world_coords = transformation_matrix @ camera_coords
            
            return float(world_coords[0]), float(world_coords[1]), 0.0  # Assuming ground level
            
        except Exception as e:
            carb.log_error(f"Coordinate transformation failed: {str(e)}")
            return camera_x * 0.01, camera_y * 0.01, 0.0
    
    def get_calibrated_cameras(self) -> List[str]:
        """Get list of calibrated cameras."""
        return list(self._calibration_data.keys())
    
    def is_camera_calibrated(self, camera_name: str) -> bool:
        """Check if a camera is calibrated."""
        return camera_name in self._calibration_data
    
    def get_calibration_accuracy(self, camera_name: str) -> float:
        """Get calibration accuracy score for a camera."""
        if camera_name not in self._calibration_data:
            return 0.0
        
        # Calculate accuracy based on calibration point distribution and matrix condition
        try:
            transformation_matrix = np.array(self._calibration_data[camera_name]['transformation_matrix'])
            condition_number = np.linalg.cond(transformation_matrix)
            
            # Lower condition number means better calibration
            # Convert to 0-100 scale where 100 is perfect
            accuracy = max(0, min(100, 100 - (condition_number - 1) * 10))
            return accuracy
            
        except Exception:
            return 0.0


# Global instance
camera_calibration_manager = CameraCalibrationManager()
