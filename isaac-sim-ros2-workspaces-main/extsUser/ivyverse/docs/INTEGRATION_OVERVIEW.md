# Extension Integration Overview

```mermaid
graph TD
    A[Ivyverse Extension] --> B[Kit Application]
    B --> C[.kit Configuration File]
    
    C --> D[Dependencies Section]
    C --> E[Settings Section]
    
    D --> F["omni.ivyverse = {}"]
    E --> G[Extension Settings]
    
    B --> H[Extension Manager]
    H --> I[Enable/Disable]
    H --> J[Configure API Keys]
    
    A --> K[Extension Files]
    K --> L[extension.toml]
    K --> M[Python Modules]
    K --> N[UI Components]
```

## File Structure

```
kit-extension-ivyverse/
├── docs/
│   └── ADDING_TO_APPLICATION.md    # This guide
├── exts/
│   └── omni.ivyverse/
│       ├── config/
│       │   └── extension.toml      # Extension configuration
│       └── omni/
│           └── ivyverse/
│               ├── extension.py    # Main extension class
│               ├── window.py       # UI window
│               ├── llm_manager.py  # LLM integration
│               └── scene_analyzer.py # USD scene analysis
└── README.md                       # Main documentation

kit-app-template/
├── templates/
│   └── apps/
│       ├── kit_base_editor/
│       │   └── kit_base_editor.kit  # App configuration
│       └── usd_viewer/
│           └── usd_viewer.kit       # App configuration
└── exts/                           # Extensions folder (symlinks here)
```

## Integration Flow

1. **Development Phase**:
   - Create extension in `kit-extension-ivyverse`
   - Link to `kit-app-template/exts/`
   - Test with standalone scripts

2. **Integration Phase**:
   - Choose target application (.kit file)
   - Add extension to dependencies
   - Configure settings

3. **Runtime Phase**:
   - Kit loads .kit configuration
   - Resolves dependencies
   - Loads Ivyverse extension
   - UI appears in Omniverse

4. **Usage Phase**:
   - User configures API keys
   - Loads USD scenes
   - Interacts with Ivyverse chat
