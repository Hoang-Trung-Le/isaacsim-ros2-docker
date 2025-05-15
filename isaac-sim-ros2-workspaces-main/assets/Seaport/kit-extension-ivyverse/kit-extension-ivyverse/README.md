# Ivyverse Extension

This is the Ivyverse extension for NVIDIA Omniverse, providing an AI-powered copilot for USD scene analysis and interaction.

## Quick Start

1. **Link the extension** to your Omniverse application:
   ```bash
   cd kit-extension-ivyverse
   ./link_app.sh  # On Linux/Mac
   # or
   link_app.bat   # On Windows
   ```

2. **Add to your application** - see [Adding to Application Guide](docs/ADDING_TO_APPLICATION.md)

3. **Configure API keys** through the extension UI or environment variables

## Documentation

- [Adding to Application](docs/ADDING_TO_APPLICATION.md) - How to integrate with your Kit app
- [Standalone Testing](standalone_test/README.md) - Test without Omniverse
- [Quick Reference](standalone_test/QUICK_REFERENCE.md) - Command reference

## Features

- Natural language scene querying
- Support for NVIDIA NIM and OpenAI GPT models
- Real-time scene context awareness
- Export conversation and analysis reports

## Development

To develop or test the extension:

1. Clone this repository
2. Link to your kit-app-template
3. Enable in your Omniverse application
4. Configure your LLM API keys

For detailed instructions, see the documentation links above.
