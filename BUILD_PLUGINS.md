# Plugin Build Script (`plugins_build.py`)

This script automates the generation of the plugin manifest JSON file (e.g., `default_plugins.json` and `optional_plugins.json`) by scanning the source code of plugins.

## Features
- **Zero Dependencies**: Uses Python's built-in `ast` module to parse code statically. No need to install plugin dependencies to run the build script.
- **Metadata Extraction**: automatically extracts `id`, `name`, `version`, `icon` paths, and other metadata from the `Plugin` class initialization.

## Usage

Run the script from the terminal:

```bash
python3 build_plugins.py [options]
```

### Arguments

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--plugins-dir` | `./plugins` | Path to the directory containing plugin folders. |
| `--output` | `plugins.json` | Path where the generated JSON file will be saved. |
| `--version` | Current Date (`YYYY.MM.DD-alpha`) | version string to apply to the manifest. |
| `--url-base` | `None` | Optional base URL to construct download links (e.g., `https://example.com/downloads`). |
| `--downloads-dir` | `None` | Directory to save plugin zip archives. If provided, creates a zip file for each plugin. |

### Examples

**Generate `optional_plugins.json` from local plugins:**

```bash
python3 build_plugins.py --output plugins/optional_plugins.json --downloads-dir ./downloads --url-base https://github.com/Resistine/Resistine-Desktop-Plugins/releases/download/2026.01.04-alpha/

**Generate `default_plugins.json` and create zip archives:**

```bash
python3 build_plugins.py --plugins-dir ../Resistine-Desktop/plugins --output plugins/default_plugins.json --downloads-dir ./downloads --url-base https://github.com/Resistine/Resistine-Desktop-Plugins/releases/download/2026.01.04-alpha/
```

## Requirements
- Python 3.6+
