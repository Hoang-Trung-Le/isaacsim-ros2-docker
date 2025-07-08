import importlib
import os

from .usd_meta_functions_get import *
from .usd_meta_functions_set import *

# Get the directory of metafunction_modules
metafunction_modules_dir = os.path.join(os.path.dirname(__file__), "metafunction_modules")

# List of module names to import
module_files = [f for f in os.listdir(metafunction_modules_dir) if f.endswith(".py") and f != "__init__.py"]
module_names = [os.path.splitext(f)[0] for f in module_files]

# Import all the modules and add them to the current module's namespace
for module_name in module_names:
    if module_name.startswith("__"):
        continue
    imported_module = importlib.import_module(f".metafunction_modules.{module_name}", package=__name__)
    globals()[module_name] = imported_module
