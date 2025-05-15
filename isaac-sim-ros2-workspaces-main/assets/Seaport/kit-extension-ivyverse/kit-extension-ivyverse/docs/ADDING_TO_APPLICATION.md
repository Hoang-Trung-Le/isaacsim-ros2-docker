# Adding Ivyverse Extension to Your Omniverse Application

This guide explains how to integrate the Ivyverse extension into your Omniverse Kit application.

## Overview

When developing an Omniverse extension, you need to configure your Kit application to load the extension. This is done through Kit configuration files (`.kit` files) which define application settings, dependencies, and behavior.

## Prerequisites

1. The Ivyverse extension is properly linked to your kit-app-template
2. You have a working Omniverse Kit application
3. You know the location of your application's `.kit` configuration file

## Methods to Add the Extension

### Method 1: Adding to Existing .kit File

The most common approach is to add your extension to an existing application's `.kit` file.

1. **Locate your .kit file**:
   - For kit-app-template: `/templates/apps/*/[app_name].kit`
   - Common examples:
     - `/templates/apps/kit_base_editor/kit_base_editor.kit`
     - `/templates/apps/usd_composer/usd_composer.kit`
     - `/templates/apps/usd_viewer/usd_viewer.kit`

2. **Edit the .kit file**:
   Open the file and find the `[dependencies]` section:
   ```toml
   [dependencies]
   "omni.kit.mainwindow" = {}
   "omni.kit.viewport.window" = {}
   # ... other extensions ...
   ```

3. **Add your extension**:
   ```toml
   [dependencies]
   "omni.kit.mainwindow" = {}
   "omni.kit.viewport.window" = {}
   # ... other extensions ...
   "omni.ivyverse" = {}  # Add this line
   ```

### Method 2: Creating a Custom .kit File

Create a new application configuration specifically for using Ivyverse:

1. **Create a new file**: `my_app_with_ivyverse.kit`

2. **Add configuration**:
   ```toml
   [package]
   title = "USD Scene Analysis with Ivyverse"
   version = "1.0.0"
   description = "Application with Ivyverse AI copilot"
   keywords = ["app", "usd", "ai"]

   [dependencies]
   # Core Kit functionality
   "omni.kit.mainwindow" = {}
   "omni.kit.viewport.window" = {}
   "omni.kit.menu.file" = {}
   "omni.kit.menu.edit" = {}
   "omni.kit.window.stage" = {}
   "omni.kit.window.property" = {}
   
   # USD functionality
   "omni.usd" = {}
   "omni.hydra.rtx" = {}
   
   # Ivyverse extension
   "omni.ivyverse" = {}

   [settings]
   # Auto-load Ivyverse on startup
   exts."omni.ivyverse".autoload = true
   
   # Application settings
   app.window.title = "USD Viewer with Ivyverse"
   app.content.emptyStageOnStart = false
   ```

### Method 3: Extension Auto-loading

Configure the extension itself to auto-load by modifying its `extension.toml`:

```toml
[settings]
exts."omni.ivyverse".autoload = true
```

This is already configured in your extension.

## Configuration Options

### Basic Dependency

```toml
"omni.ivyverse" = {}
```

### With Version Specification

```toml
"omni.ivyverse" = { version = "1.0.0" }
```

### With Order Priority

```toml
"omni.ivyverse" = { order = 100 }  # Load after other extensions
```

### With Optional Flag

```toml
"omni.ivyverse" = { optional = true }  # Won't fail if not found
```

## Complete Example

Here's a complete example of a minimal Kit application with Ivyverse:

```toml
[package]
title = "Ivyverse Scene Analyzer"
version = "1.0.0"
description = "USD scene analysis with AI assistance"
keywords = ["app", "usd", "ai", "copilot"]

[dependencies]
# Core UI
"omni.kit.mainwindow" = {}
"omni.kit.uiapp" = {}

# Viewport
"omni.kit.viewport.window" = {}
"omni.hydra.rtx" = {}

# USD support
"omni.usd" = {}
"omni.kit.window.stage" = {}

# Menus
"omni.kit.menu.file" = {}
"omni.kit.menu.edit" = {}

# Property editor
"omni.kit.window.property" = {}

# Ivyverse extension
"omni.ivyverse" = { order = 1000 }  # Load last

[settings]
# Window settings
app.window.title = "Ivyverse - USD Scene Copilot"
app.window.width = 1920
app.window.height = 1080

# Content settings
app.content.emptyStageOnStart = false

# Extension settings
exts."omni.ivyverse".autoload = true

# Viewport settings
app.viewport.defaults.fillViewport = true

[settings.app.exts]
folders.'++' = [
    "${app}/../exts",
    "${app}/../extscache/"
]
```

## Verifying the Installation

1. **Check extension is loaded**:
   - Open Window > Extensions
   - Search for "Ivyverse"
   - Verify it's enabled

2. **Check for the window**:
   - Look for "Ivyverse - Scene Copilot" in the Window menu
   - Or use the extension manager to open it

3. **Test functionality**:
   - Load a USD scene
   - Open the Ivyverse window
   - Try commands like `overview` or `objects`

## Troubleshooting

### Extension Not Found

If the extension isn't found:

1. Verify the extension is properly linked:
   ```bash
   ls -la /path/to/kit-app-template/exts/
   ```
   Should show `omni.ivyverse` symlink

2. Check the extension search paths in your .kit file:
   ```toml
   [settings.app.exts]
   folders.'++' = [
       "${app}/../exts",
       "${app}/../../../kit-extension-ivyverse/exts"  # Add direct path
   ]
   ```

### Extension Not Loading

If the extension is found but not loading:

1. Check the console for errors
2. Verify all dependencies are available
3. Check the extension.toml is valid
4. Ensure API keys are configured (if needed)

### API Keys Configuration

The extension needs API keys for LLM functionality:

1. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-key"
   # or
   export NVIDIA_NIM_API_KEY="your-key"
   ```

2. Or configure in the extension UI after loading

## Best Practices

1. **Development Setup**: Use a dedicated .kit file for development
2. **Production Setup**: Include only necessary dependencies
3. **Version Control**: Specify exact versions for production
4. **Documentation**: Document any custom settings or requirements

## Resources

- [Kit Manual](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/index.html)
- [Extension Development](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/extensions.html)
- [Kit Configuration](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/configuration.html)
