"""
OmniAlert Extension Entry Point
Minimal initialization for window UI only
"""

import omni.ext
import omni.ui as ui
import omni.kit.menu.utils
import carb
from typing import Optional

from .window import OmniAlertWindow


class OmniAlertExtension(omni.ext.IExt):
    """OmniAlert extension main class - minimal version"""

    def __init__(self):
        super().__init__()
        carb.log_info("[OmniAlertExtension] Extension __init__ called")

        # Initialize attributes with defensive programming
        self._window: Optional[OmniAlertWindow] = None
        self._menu_items = []
        self._initialized = False

        carb.log_info("[OmniAlertExtension] Extension object created successfully")

    @property
    def window(self) -> Optional[OmniAlertWindow]:
        """Property to ensure _window attribute always exists"""
        if not hasattr(self, "_window"):
            carb.log_warn(
                "[OmniAlertExtension] _window attribute missing, initializing via property..."
            )
            self._window = None
        return self._window

    @window.setter
    def window(self, value: Optional[OmniAlertWindow]):
        """Setter for window property"""
        self._window = value

    def _ensure_attributes(self):
        """Ensure all required attributes exist"""
        if not hasattr(self, "_window"):
            carb.log_warn("[OmniAlertExtension] _window missing, initializing...")
            self._window = None
        if not hasattr(self, "_menu_items"):
            carb.log_warn("[OmniAlertExtension] _menu_items missing, initializing...")
            self._menu_items = []
        if not hasattr(self, "_initialized"):
            carb.log_warn("[OmniAlertExtension] _initialized missing, initializing...")
            self._initialized = False

    def on_startup(self, ext_id: str):
        """Extension startup - minimal initialization"""
        carb.log_info("[OmniAlertExtension] Starting extension...")
        carb.log_info(f"[OmniAlertExtension] Extension ID: {ext_id}")

        try:
            # Ensure we have the required attributes
            self._ensure_attributes()

            # Register simple menu items without icons
            self._register_menu_items()

            self._initialized = True
            carb.log_info("[OmniAlertExtension] Extension startup complete")

        except Exception as e:
            carb.log_error(f"[OmniAlertExtension] Startup failed: {e}")
            import traceback

            carb.log_error(f"[OmniAlertExtension] Traceback: {traceback.format_exc()}")

    def on_shutdown(self):
        """Extension shutdown"""
        carb.log_info("[OmniAlertExtension] Starting extension shutdown...")

        try:
            # Ensure attributes exist before checking
            self._ensure_attributes()

            # Clean shutdown with defensive checks
            if self._window:
                carb.log_info("[OmniAlertExtension] Destroying window...")
                self._window.destroy()
                self._window = None
                carb.log_info("[OmniAlertExtension] Window destroyed")
            else:
                carb.log_info("[OmniAlertExtension] No window to destroy")

            # Remove menu items
            self._remove_menu_items()

            carb.log_info("[OmniAlertExtension] Extension shutdown complete")

        except Exception as e:
            carb.log_error(f"[OmniAlertExtension] Shutdown error: {e}")
            import traceback

            carb.log_error(f"[OmniAlertExtension] Traceback: {traceback.format_exc()}")

    def _register_menu_items(self):
        """Register simple menu items without icons"""
        try:
            carb.log_info("[OmniAlertExtension] Registering menu items...")

            # Ensure attributes exist
            self._ensure_attributes()

            # Create menu item descriptions
            self._menu_items = [
                omni.kit.menu.utils.MenuItemDescription(
                    name="OmniAlert Dashboard",
                    ticked=True,
                    ticked_fn=self._is_window_visible,
                    onclick_fn=self._toggle_window,
                )
                # omni.kit.menu.utils.MenuItemDescription(
                #     name="OmniAlert Debug Test",
                #     onclick_fn=self._show_debug_test,
                # ),
            ]

            # Add menu items to Window menu
            omni.kit.menu.utils.add_menu_items(self._menu_items, "Window")
            carb.log_info("[OmniAlertExtension] Menu items registered successfully")

        except Exception as e:
            carb.log_error(f"[OmniAlertExtension] Menu registration failed: {e}")
            import traceback

            carb.log_error(f"[OmniAlertExtension] Traceback: {traceback.format_exc()}")

    def _remove_menu_items(self):
        """Remove menu items"""
        try:
            carb.log_info("[OmniAlertExtension] Removing menu items...")

            # Ensure attributes exist
            self._ensure_attributes()

            if self._menu_items:
                # Remove menu items using the proper utility function
                omni.kit.menu.utils.remove_menu_items(self._menu_items, "Window")
                carb.log_info("[OmniAlertExtension] Menu items removed successfully")
                self._menu_items = []
            else:
                carb.log_info("[OmniAlertExtension] No menu items to remove")

        except Exception as e:
            carb.log_error(f"[OmniAlertExtension] Menu removal failed: {e}")
            import traceback

            carb.log_error(f"[OmniAlertExtension] Traceback: {traceback.format_exc()}")

    def _is_window_visible(self):
        """Check if window is visible"""
        return self._window and self._window.visible

    def _toggle_window(self):
        """Toggle window visibility"""
        try:
            carb.log_info("[OmniAlertExtension] Toggle window requested...")

            if not self._window:
                carb.log_info("[OmniAlertExtension] Creating new window...")
                try:
                    # Create window with simple parameters
                    self._window = OmniAlertWindow(
                        title="OmniAlert - Ivygilant - Industrial Alert System",
                        width=800,
                        height=600,
                    )
                    carb.log_info("[OmniAlertExtension] Window created successfully")
                except Exception as window_error:
                    carb.log_error(
                        f"[OmniAlertExtension] Window creation failed: {window_error}"
                    )
                    import traceback

                    carb.log_error(
                        f"[OmniAlertExtension] Window creation traceback: {traceback.format_exc()}"
                    )
                    return

            # Toggle visibility
            if self._window:
                old_visibility = self._window.visible
                self._window.visible = not self._window.visible
                carb.log_info(
                    f"[OmniAlertExtension] Window visibility changed: {old_visibility} -> {self._window.visible}"
                )
                # Refresh menu to update tick mark
                omni.kit.menu.utils.refresh_menu_items("Window")
            else:
                carb.log_error(
                    "[OmniAlertExtension] Window is None, cannot change visibility"
                )

        except Exception as e:
            carb.log_error(f"[OmniAlertExtension] Window toggle failed: {e}")
            import traceback

            carb.log_error(
                f"[OmniAlertExtension] Full traceback: {traceback.format_exc()}"
            )

    def _show_window(self, *args):
        """Show/hide main window with debug logging (legacy method)"""
        self._toggle_window()

    # def _show_debug_test(self, *args):
    #     """Show debug test information"""
    #     try:
    #         carb.log_info("[OmniAlertExtension] Debug test requested...")

    #         # Ensure attributes exist
    #         self._ensure_attributes()

    #         # Check object state
    #         carb.log_info(f"[OmniAlertExtension] Object type: {type(self)}")
    #         carb.log_info(f"[OmniAlertExtension] Object dict: {self.__dict__}")
    #         carb.log_info(
    #             f"[OmniAlertExtension] Has _window attribute: {hasattr(self, '_window')}"
    #         )
    #         carb.log_info(
    #             f"[OmniAlertExtension] Has _initialized attribute: {hasattr(self, '_initialized')}"
    #         )
    #         carb.log_info(
    #             f"[OmniAlertExtension] Initialized: {getattr(self, '_initialized', 'Unknown')}"
    #         )

    #         # Test window property
    #         carb.log_info(f"[OmniAlertExtension] Window property: {self._window}")
    #         carb.log_info(
    #             f"[OmniAlertExtension] Window exists: {self._window is not None}"
    #         )

    #         if self._window:
    #             carb.log_info(
    #                 f"[OmniAlertExtension] Window visible: {self._window.visible}"
    #             )
    #             carb.log_info(
    #                 f"[OmniAlertExtension] Window initialized: {getattr(self._window, 'window_initialized', 'Unknown')}"
    #             )

    #         carb.log_info("[OmniAlertExtension] Debug test complete")

    #     except Exception as e:
    #         carb.log_error(f"[OmniAlertExtension] Debug test failed: {e}")
    #         import traceback

    #         carb.log_error(f"[OmniAlertExtension] Traceback: {traceback.format_exc()}")


# # Global access functions (simplified)
# _extension_instance: Optional[OmniAlertExtension] = None


# def get_extension_instance() -> Optional[OmniAlertExtension]:
#     """Get the extension instance"""
#     carb.log_info("[OmniAlertExtension] Extension instance requested")
#     return _extension_instance


# def create_extension_instance() -> OmniAlertExtension:
#     """Create extension instance"""
#     global _extension_instance
#     carb.log_info("[OmniAlertExtension] Creating extension instance...")
#     _extension_instance = OmniAlertExtension()
#     carb.log_info("[OmniAlertExtension] Extension instance created")
#     return _extension_instance
