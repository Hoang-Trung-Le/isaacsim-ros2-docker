# Installation Guide

This guide provides step-by-step instructions for installing and configuring the OmniAlert extension in NVIDIA Omniverse Isaac Sim.

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11 or Linux (Ubuntu 20.04/22.04 recommended)
- **GPU**: NVIDIA RTX capable GPU (Turing or newer recommended)
- **Driver**: Latest NVIDIA driver compatible with your GPU
- **Omniverse**: Isaac Sim 2023.1.0 or later
- **Python**: Python 3.7+ (included with Isaac Sim)
- **Internet Access**: Required for API connectivity (optional for local use)

### Dependencies

The extension requires the following Omniverse dependencies (automatically resolved):

- `omni.kit.uiapp`
- `omni.kit.viewport.window`
- `omni.usd`
- `omni.kit.window.property`
- `omni.isaac.core`
- `omni.kit.window.extensions`
- `omni.ui`
- `omni.kit.commands`

## Installation Methods

### Method 1: Extension Manager (Recommended)

1. **Open Isaac Sim**:
   - Launch NVIDIA Omniverse Isaac Sim
   - Wait for the application to fully load

2. **Access Extension Manager**:
   - Go to `Window` → `Extensions`
   - The Extension Manager window will open

3. **Install OmniAlert**:
   - In the search bar, type "OmniAlert"
   - Locate "OmniAlert - Ivygilant - Industrial Alert System"
   - Click the toggle switch to enable the extension
   - The extension will automatically download and install

4. **Verify Installation**:
   - Check that the extension appears in the "Enabled" section
   - Look for the OmniAlert menu in `Window` → `OmniAlert Dashboard`

### Method 2: Manual Installation

1. **Download Extension**:
   - Download the OmniAlert extension package
   - Extract the contents to get the `OmniAlert` folder

2. **Copy to Extensions Directory**:
   ```bash
   # Windows
   C:\Users\{username}\AppData\Local\ov\pkg\isaac_sim\extsUser\OmniAlert\
   
   # Linux
   ~/.local/share/ov/pkg/isaac_sim/extsUser/OmniAlert/
   ```

3. **Enable Extension**:
   - Open Isaac Sim
   - Go to `Window` → `Extensions`
   - Click the "Refresh" button
   - Find "OmniAlert" in the list and enable it

### Method 3: Development Installation

For developers who want to modify the extension:

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd OmniAlert
   ```

2. **Create Symbolic Link**:
   ```bash
   # Windows (as Administrator)
   mklink /D "C:\Users\{username}\AppData\Local\ov\pkg\isaac_sim\extsUser\OmniAlert" "path\to\cloned\OmniAlert"
   
   # Linux
   ln -s /path/to/cloned/OmniAlert ~/.local/share/ov/pkg/isaac_sim/extsUser/OmniAlert
   ```

3. **Enable Development Mode**:
   - In Extension Manager, enable "Developer Mode"
   - Refresh extensions list
   - Enable OmniAlert extension

## Post-Installation Configuration

### Initial Setup

1. **Open OmniAlert**:
   - Go to `Window` → `OmniAlert Dashboard`
   - The main OmniAlert window will appear

2. **Verify Installation**:
   - Check that all tabs are accessible (Dashboard, Alerts, Analytics, API, Settings)
   - Verify no error messages appear in the console

### API Configuration (Optional)

If you plan to use external alert sources:

1. **Navigate to API Tab**:
   - Click the "🔗 API" tab in the OmniAlert window

2. **Configure Connection**:
   - **Base URL**: Enter your API server URL (e.g., `http://localhost:8000`)
   - **API Key**: Enter your authentication key (if required)
   - **WebSocket URL**: Enter WebSocket endpoint (e.g., `ws://localhost:8000/ws`)
   - **Polling Interval**: Set alert polling frequency (default: 10 seconds)

3. **Test Connection**:
   - Click "🧪 Test Connection"
   - Verify successful connection in console logs

### Camera Settings

Configure camera behavior for alert navigation:

1. **Navigate to Settings Tab**:
   - Click the "⚙️ Settings" tab

2. **Adjust Camera Settings**:
   - **Animation Duration**: Camera movement speed (default: 2.0 seconds)
   - **Smooth Transitions**: Enable smooth camera animations
   - **Auto Frame Objects**: Automatically frame objects when navigating
   - **Camera Distance**: Default distance from alert locations

### Notification Settings

Customize alert notifications:

1. **In Settings Tab**:
   - Configure notification timeout (default: 5 seconds)
   - Set maximum simultaneous notifications
   - Enable/disable sound alerts
   - Configure severity filters

## Verification

### Basic Functionality Test

1. **Create Test Alert**:
   - Go to the "Alerts" tab
   - Scroll down to "Test Alert Creation"
   - Select alert template and severity
   - Enter location coordinates (0, 0, 0 for default)
   - Click "Create Test Alert"

2. **Verify Alert Display**:
   - Check that alert appears in the dashboard
   - Verify notification popup appears
   - Test acknowledge and resolve buttons

3. **Test Camera Navigation**:
   - Click the "🔍 View" button on an alert
   - Verify camera moves to the specified location
   - Check animation smoothness

### Advanced Features Test

1. **Test Filtering**:
   - Create multiple test alerts with different severities
   - Use filter controls to show/hide alerts
   - Test search functionality

2. **Test Export**:
   - Create several test alerts
   - Click "📤 Export" button
   - Verify export file is generated

3. **Test Emergency Stop**:
   - Create critical test alerts
   - Click the "🚨 EMERGENCY" button
   - Verify all notifications are dismissed

## Troubleshooting

### Common Installation Issues

#### Extension Not Found

**Problem**: OmniAlert doesn't appear in Extension Manager

**Solutions**:
- Refresh the extensions list
- Check that files are in the correct directory
- Verify `extension.toml` file is present and valid
- Check console for loading errors

#### Permission Errors

**Problem**: Cannot copy files to extensions directory

**Solutions**:
- Run Isaac Sim as Administrator (Windows)
- Check directory permissions
- Use alternative installation directory
- Verify antivirus software isn't blocking

#### Missing Dependencies

**Problem**: Extension fails to load due to missing dependencies

**Solutions**:
- Verify Isaac Sim version compatibility
- Check that all required extensions are enabled
- Update Isaac Sim to the latest version
- Clear extension cache and reload

### Runtime Issues

#### UI Not Displaying

**Problem**: OmniAlert window is blank or corrupted

**Solutions**:
- Restart Isaac Sim
- Reset window layout in Isaac Sim
- Check console for UI-related errors
- Disable and re-enable the extension

#### API Connection Failures

**Problem**: Cannot connect to external alert sources

**Solutions**:
- Verify network connectivity
- Check API server is running
- Validate API endpoint URLs
- Review API key authentication
- Check firewall settings

#### Camera Navigation Issues

**Problem**: Camera doesn't move to alert locations

**Solutions**:
- Verify alert has valid location data
- Check that USD prims exist at specified paths
- Adjust camera animation settings
- Verify viewport is active

### Getting Help

#### Console Logs

Always check the Isaac Sim console for detailed error messages:

- Look for `[OmniAlert]` prefixed messages
- Note any ERROR or WARNING messages
- Copy relevant log entries for support requests

#### Log Files

Find detailed logs in:
```bash
# Windows
%USERPROFILE%\.nvidia-omniverse\logs\Kit\Isaac-Sim\

# Linux
~/.nvidia-omniverse/logs/Kit/Isaac-Sim/
```

#### Support Channels

1. **Documentation**: Review README.md and API_INTEGRATION.md
2. **Error Codes**: Check error messages against documentation
3. **Community Forums**: Post issues with detailed error logs
4. **Development**: For code issues, check the extension source code

## Uninstallation

### Method 1: Extension Manager

1. Open Extension Manager (`Window` → `Extensions`)
2. Find "OmniAlert" in the enabled extensions
3. Click the toggle to disable
4. Optionally, click the gear icon and select "Remove"

### Method 2: Manual Removal

1. **Disable Extension** (if enabled):
   - Use Extension Manager to disable first

2. **Remove Files**:
   ```bash
   # Windows
   rmdir /s "C:\Users\{username}\AppData\Local\ov\pkg\isaac_sim\extsUser\OmniAlert"
   
   # Linux
   rm -rf ~/.local/share/ov/pkg/isaac_sim/extsUser/OmniAlert
   ```

3. **Clear Cache** (optional):
   - Restart Isaac Sim to clear any cached data

## Updating

### Automatic Updates

If installed via Extension Manager:
1. Extension Manager will show update notifications
2. Click "Update" when available
3. Restart Isaac Sim if prompted

### Manual Updates

For manual installations:
1. Download the new version
2. Disable the current extension
3. Replace files in the installation directory
4. Re-enable the extension
5. Restart Isaac Sim

## Development Setup

For developers wanting to modify or contribute:

### Prerequisites

- Git version control
- Text editor or IDE (VS Code recommended)
- Python development environment
- Basic understanding of Omniverse extensions

### Development Installation

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd OmniAlert
   ```

2. **Set Up Development Environment**:
   - Install development dependencies
   - Configure IDE for Python development
   - Set up debugging configuration

3. **Link to Isaac Sim**:
   - Create symbolic link to extensions directory
   - Enable developer mode in Extension Manager
   - Enable extension and test changes

### Development Workflow

1. **Make Changes**: Edit extension files
2. **Test**: Reload extension in Isaac Sim
3. **Debug**: Use console logs and debugger
4. **Document**: Update documentation as needed
5. **Commit**: Use git for version control

## Next Steps

After successful installation:

1. **Read User Guide**: Review README.md for usage instructions
2. **Configure API**: Set up connections to your alert systems
3. **Test Integration**: Create test alerts and verify functionality
4. **Customize Settings**: Adjust behavior to match your workflow
5. **Train Users**: Ensure operators understand the interface

For detailed usage instructions, see the main README.md file.
For API integration, see API_INTEGRATION.md. 