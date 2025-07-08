"""
Camera Controller for OmniAlert Extension
Handles camera navigation and focus functionality for alert prims
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import carb
import omni.usd
import omni.kit.commands
from omni.kit.viewport.utility import get_active_viewport, frame_viewport_selection
from pxr import Usd, UsdGeom, Gf, Sdf

from .alert_types import AlertLocation


class CameraController:
    """
    Camera controller for navigating to alert locations
    Focuses on prim framing using official Omniverse APIs
    """

    def __init__(self):
        self._viewport = None
        self._camera_path = None
        self._zoom_factor = 0.6  # For FramePrimsCommand

        # Navigation history for undo functionality
        self._navigation_history: List[Dict[str, Any]] = []
        self._max_history = 10

        self._initialize_viewport()
        carb.log_info("[CameraController] Initialized")

    def _initialize_viewport(self) -> bool:
        """Initialize viewport and camera references"""
        try:
            # Get active viewport using official API
            self._viewport = get_active_viewport()
            if not self._viewport:
                carb.log_error("[CameraController] No active viewport found")
                return False

            # Get active camera path
            self._camera_path = self._viewport.camera_path
            carb.log_info("[CameraController] Viewport initialized successfully")
            return True

        except Exception as e:
            carb.log_error(f"[CameraController] Failed to initialize viewport: {e}")
            return False

    def _save_current_camera_state(self) -> Dict[str, Any]:
        """Save current camera state for history/undo"""
        try:
            if not self._camera_path:
                return {}

            stage = omni.usd.get_context().get_stage()
            if not stage:
                return {}

            camera_prim = stage.GetPrimAtPath(self._camera_path)
            if not camera_prim:
                return {}

            # Get camera transform
            xformable = UsdGeom.Xformable(camera_prim)
            transform_matrix = xformable.GetLocalTransformation()
            position = transform_matrix.ExtractTranslation()

            state = {
                "camera_path": str(self._camera_path),
                "position": (position[0], position[1], position[2]),
                "timestamp": datetime.now().isoformat(),
            }

            # Add to history
            self._navigation_history.append(state)
            if len(self._navigation_history) > self._max_history:
                self._navigation_history.pop(0)

            return state

        except Exception as e:
            carb.log_error(f"[CameraController] Failed to save camera state: {e}")
            return {}

    def focus_on_prim(self, prim_path: str, use_advanced: bool = True) -> bool:
        """
        Focus camera on a specific prim (main method for alerts)

        Args:
            prim_path: USD prim path to focus on
            use_advanced: Use advanced FramePrimsCommand (True) or basic framing (False)

        Returns:
            bool: True if successful
        """
        try:
            if not self._viewport:
                carb.log_error("[CameraController] No viewport available")
                return False

            stage = omni.usd.get_context().get_stage()
            if not stage:
                return False

            prim = stage.GetPrimAtPath(prim_path)
            if not prim:
                carb.log_warn(f"[CameraController] Prim not found: {prim_path}")
                return False

            # Save current state for undo
            self._save_current_camera_state()

            # Use advanced or basic framing
            if use_advanced:
                success = self._frame_prim_advanced(prim_path)
                if not success:
                    carb.log_warn(
                        "[CameraController] Advanced framing failed, trying basic"
                    )
                    success = self._frame_prim_basic(prim_path)
            else:
                success = self._frame_prim_basic(prim_path)

            if success:
                carb.log_info(
                    f"[CameraController] Successfully focused on prim: {prim_path}"
                )

            return success

        except Exception as e:
            carb.log_error(
                f"[CameraController] Failed to focus on prim {prim_path}: {e}"
            )
            return False

    def _frame_prim_basic(self, prim_path: str) -> bool:
        """Focus camera on prim using basic framing (fallback method)"""
        try:
            if not self._viewport:
                return False

            # Set selection and frame it using official API
            ctx = omni.usd.get_context()
            ctx.get_selection().set_selected_prim_paths([prim_path], True)
            frame_viewport_selection(self._viewport)

            carb.log_info(f"[CameraController] Framed prim (basic): {prim_path}")
            return True

        except Exception as e:
            carb.log_error(
                f"[CameraController] Failed to frame prim (basic) {prim_path}: {e}"
            )
            return False

    def _frame_prim_advanced(self, prim_path: str) -> bool:
        """Focus camera on prim using advanced FramePrimsCommand (preferred method)"""
        try:
            if not self._viewport:
                return False

            stage = omni.usd.get_context().get_stage()
            if not stage:
                return False

            # Get viewport information for FramePrimsCommand
            time_code = getattr(self._viewport, "time", Usd.TimeCode.Default())
            resolution = getattr(self._viewport, "resolution", (1920, 1080))
            camera_path = self._viewport.camera_path

            # Calculate aspect ratio
            aspect_ratio = resolution[0] / resolution[1] if resolution[1] != 0 else 1.0

            # Execute FramePrimsCommand using official API
            omni.kit.commands.execute(
                "FramePrimsCommand",
                prim_to_move=camera_path,
                prims_to_frame=[prim_path],
                time_code=time_code,
                aspect_ratio=aspect_ratio,
                zoom=self._zoom_factor,
            )

            carb.log_info(f"[CameraController] Framed prim (advanced): {prim_path}")
            return True

        except Exception as e:
            carb.log_error(
                f"[CameraController] Failed to frame prim (advanced) {prim_path}: {e}"
            )
            return False

    def focus_on_multiple_prims(
        self, prim_paths: List[str], use_advanced: bool = True
    ) -> bool:
        """
        Focus camera on multiple prims simultaneously

        Args:
            prim_paths: List of USD prim paths to focus on
            use_advanced: Use advanced FramePrimsCommand

        Returns:
            bool: True if successful
        """
        try:
            if not prim_paths:
                return False

            if not self._viewport:
                carb.log_error("[CameraController] No viewport available")
                return False

            # Save current state
            self._save_current_camera_state()

            if use_advanced:
                # Use FramePrimsCommand for multiple prims
                time_code = getattr(self._viewport, "time", Usd.TimeCode.Default())
                resolution = getattr(self._viewport, "resolution", (1920, 1080))
                camera_path = self._viewport.camera_path
                aspect_ratio = (
                    resolution[0] / resolution[1] if resolution[1] != 0 else 1.0
                )

                omni.kit.commands.execute(
                    "FramePrimsCommand",
                    prim_to_move=camera_path,
                    prims_to_frame=prim_paths,
                    time_code=time_code,
                    aspect_ratio=aspect_ratio,
                    zoom=self._zoom_factor,
                )

                carb.log_info(
                    f"[CameraController] Framed multiple prims (advanced): {len(prim_paths)} prims"
                )
                return True
            else:
                # Use basic selection framing
                ctx = omni.usd.get_context()
                ctx.get_selection().set_selected_prim_paths(prim_paths, True)
                frame_viewport_selection(self._viewport)

                carb.log_info(
                    f"[CameraController] Framed multiple prims (basic): {len(prim_paths)} prims"
                )
                return True

        except Exception as e:
            carb.log_error(f"[CameraController] Failed to focus on multiple prims: {e}")
            return False

    def set_active_camera(self, camera_path: str) -> bool:
        """Change the active camera using official API"""
        try:
            if not self._viewport:
                carb.log_error("[CameraController] No viewport available")
                return False

            # Set the viewport's active camera
            self._viewport.camera_path = camera_path
            self._camera_path = camera_path

            carb.log_info(f"[CameraController] Changed active camera to: {camera_path}")
            return True

        except Exception as e:
            carb.log_error(f"[CameraController] Failed to set active camera: {e}")
            return False

    def go_back(self) -> bool:
        """Navigate back to previous camera position"""
        try:
            if len(self._navigation_history) < 2:
                carb.log_warn("[CameraController] No navigation history available")
                return False

            # Get previous state (skip current)
            previous_state = self._navigation_history[-2]
            previous_camera_path = previous_state["camera_path"]

            # Switch back to previous camera if it was different
            if previous_camera_path != str(self._camera_path):
                self.set_active_camera(previous_camera_path)

            carb.log_info("[CameraController] Navigated back to previous camera")
            return True

        except Exception as e:
            carb.log_error(f"[CameraController] Failed to go back: {e}")
            return False

    def set_zoom_factor(self, zoom: float) -> None:
        """
        Set zoom factor for FramePrimsCommand

        Args:
            zoom: Zoom factor (0.1 = close, 1.0 = far)
        """
        self._zoom_factor = max(0.1, min(2.0, zoom))  # Clamp between 0.1 and 2.0
        carb.log_info(f"[CameraController] Set zoom factor to: {self._zoom_factor}")

    def get_navigation_history(self) -> List[Dict[str, Any]]:
        """Get navigation history"""
        return self._navigation_history.copy()

    def clear_navigation_history(self) -> None:
        """Clear navigation history"""
        self._navigation_history.clear()
        carb.log_info("[CameraController] Cleared navigation history")

    def get_status(self) -> Dict[str, Any]:
        """Get camera controller status"""
        return {
            "viewport_available": self._viewport is not None,
            "camera_path": str(self._camera_path) if self._camera_path else None,
            "zoom_factor": self._zoom_factor,
            "navigation_history_count": len(self._navigation_history),
        }

    def shutdown(self) -> None:
        """Shutdown camera controller"""
        self._navigation_history.clear()
        carb.log_info("[CameraController] Shutdown complete")
