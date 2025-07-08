import omni.ext
import carb
from .window import EmployeeManagementWindow
from .global_variables import EXTENSION_TITLE

class EmployeeManagementExtension(omni.ext.IExt):
    """Main extension class for Employee Management System"""

    def on_startup(self, ext_id):
        """Called when the extension is starting up"""
        carb.log_info(f"[{EXTENSION_TITLE}] Starting up Employee Management Extension")
        print(f"[{EXTENSION_TITLE}] Starting up Employee Management Extension")
        
        try:
            # Initialize the main window
            self._window = EmployeeManagementWindow(
                title="Employee Management - Smart Warehouse",
                width=800,
                height=900
            )
            carb.log_info(f"[{EXTENSION_TITLE}] Extension started successfully")
            
        except Exception as e:
            carb.log_error(f"[{EXTENSION_TITLE}] Failed to start extension: {str(e)}")
            print(f"[{EXTENSION_TITLE}] Failed to start extension: {str(e)}")

    def on_shutdown(self):
        """Called when the extension is shutting down"""
        carb.log_info(f"[{EXTENSION_TITLE}] Shutting down Employee Management Extension")
        print(f"[{EXTENSION_TITLE}] Shutting down Employee Management Extension")
        
        try:
            if hasattr(self, '_window') and self._window:
                self._window.destroy()
                self._window = None
            carb.log_info(f"[{EXTENSION_TITLE}] Extension shutdown complete")
            
        except Exception as e:
            carb.log_error(f"[{EXTENSION_TITLE}] Error during shutdown: {str(e)}")
            print(f"[{EXTENSION_TITLE}] Error during shutdown: {str(e)}")
