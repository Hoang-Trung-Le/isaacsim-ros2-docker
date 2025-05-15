# Ivyverse Repository Structure

## Core Extension
```
exts/omni.ivyverse/
├── config/
│   └── extension.toml          # Extension configuration
├── docs/
│   ├── README.md              # Extension documentation
│   └── CHANGELOG.md           # Version history
├── data/
│   └── icon.png               # Icon
└── omni/
    └── ivyverse/
        ├── __init__.py        # Module initialization
        ├── extension.py       # Main extension class
        ├── window.py          # UI window implementation
        ├── scene_analyzer.py  # USD scene analysis
        ├── llm_manager.py     # LLM integration
        ├── chat_interface.py  # Chat functionality
        ├── utils.py           # Utility functions
        └── style.py           # UI styling
```

## Standalone Testing
```
standalone_test/
├── README.md                   # Standalone test documentation
├── standalone_scene_analyzer.py # Scene analyzer without Omniverse
├── standalone_llm_manager.py    # LLM manager without Omniverse
├── standalone_chat_interface.py # Chat interface without Omniverse
├── test_ivyverse.py            # Main test script
├── test_usd_setup.py           # USD setup verification
└── requirements.txt            # Python dependencies
```

## Documentation
```
docs/
├── ADDING_TO_APPLICATION.md    # Integration guide
└── INTEGRATION_OVERVIEW.md     # Visual overview
```

## Root Files
```
.
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules
├── link_app.sh               # Linux/Mac linking script
└── link_app.bat              # Windows linking script
```

## Essential Files Only

After cleanup, these are the essential files that contain the core logic:

1. **Extension Core**:
   - `extension.py` - Main extension entry point
   - `window.py` - UI implementation
   - `scene_analyzer.py` - USD scene analysis
   - `llm_manager.py` - AI integration
   - `chat_interface.py` - Chat functionality

2. **Configuration**:
   - `extension.toml` - Extension metadata
   - `requirements.txt` - Dependencies

3. **Documentation**:
   - `README.md` - Main documentation
   - Integration guides in `docs/`

All other files support these core components.
