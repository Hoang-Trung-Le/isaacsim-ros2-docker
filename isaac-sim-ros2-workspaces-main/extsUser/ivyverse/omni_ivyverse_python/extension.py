import omni.ext
from .window import IvyverseWindow
class IvyverseExtension(omni.ext.IExt):
    """Main extension class for Ivyverse"""

    def on_startup(self, ext_id):
        print("[omni.ivyverse] Starting up")
        self._window = IvyverseWindow("IvyVerse - 3D Scene Copilot", width=600, height=800)

    def on_shutdown(self):
        print("[omni.ivyverse] Shutting down")
        if self._window:
            self._window.destroy()
            self._window = None
