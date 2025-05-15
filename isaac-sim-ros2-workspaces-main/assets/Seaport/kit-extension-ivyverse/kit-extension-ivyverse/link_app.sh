#!/bin/bash
# Link the extension to the kit-app-template
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="$SCRIPT_DIR/exts/omni.ivyverse"
KIT_APP_DIR="$SCRIPT_DIR/../kit-app-template"
if [ ! -d "$KIT_APP_DIR" ]; then
    echo "Error: kit-app-template not found at $KIT_APP_DIR"
    exit 1
fi
# Create symbolic link
ln -sfn "$EXT_DIR" "$KIT_APP_DIR/exts/omni.ivyverse"
echo "Extension linked successfully to kit-app-template"
