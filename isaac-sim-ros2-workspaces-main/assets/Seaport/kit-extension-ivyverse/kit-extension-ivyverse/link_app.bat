@echo off

rem Link the extension to the kit-app-template
setlocal

set SCRIPT_DIR=%~dp0
set EXT_DIR=%SCRIPT_DIR%exts\omni.ivyverse
set KIT_APP_DIR=%SCRIPT_DIR%..\kit-app-template

if not exist "%KIT_APP_DIR%" (
    echo Error: kit-app-template not found at %KIT_APP_DIR%
    exit /b 1
)

rem Create symbolic link
mklink /D "%KIT_APP_DIR%\exts\omni.ivyverse" "%EXT_DIR%"

echo Extension linked successfully to kit-app-template
