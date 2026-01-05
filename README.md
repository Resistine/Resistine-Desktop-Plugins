# Resistine Desktop Plugins

Optional plugins for the **Resistine Desktop AI EDR App**.

Each plugin is a self-contained module that can be easily added to the Resistine Desktop App. The plugin system is designed to be flexible and extensible, allowing for easy integration of new capabilities.

## 🎯 Project Goals

The goal of this repository is to provide a central registry and source for various plugins that extend the functionality of the Resistine Desktop ecosystem. This includes:
- **Official Plugins**: Developed and maintained by the Resistine Team.
- **Third-Party Plugins**: Approved extensions from the community and partners.

## 🏗️ Architecture & UI Principles

The Resistine Desktop GUI is built with a focus on decoupling and flexibility:
- **Interface**: Accomplished using Shell and/or GUI.
- **Independence**: There should be NO functionality depending directly on the UI layers. Logic remains separate from presentation.

### Navigation Structure
The main application features a side-tab navigation system for plugins:
1.  **Dashboard**: Overview of security and system status.
2.  **Assistant Chat**: AI-powered cybersecurity assistant Resistina.
3.  **EndPoint**: EDR and endpoint management (only for registered paying users).
4.  ... other specialized plugins as WireGuard VPN or ClamAV antivirus for Linux and Mac.
5.  **Settings & Help**: System configuration.
6.  **Resistine Store**: Plugin management and discovery.

## 🏪 Resistine EndPoint Plugin Store

The store serves as the primary gateway for discovering new capabilities.
For advanced features and enterprise integrations, users are forwarded to register at [odoo.resistine.com](https://odoo.resistine.com).

**Sample Store Content:**
- **Template**: A template for creating new plugins.
- **Calculator**: A simple calculator plugin to show how plugins work.

Permanent link: https://raw.githubusercontent.com/Resistine/Resistine-Desktop-Plugins/main/plugins/optional_plugins.json


## 🚀 How to Test Run Plugins

To run the plugins, use the `./run.sh` script.
It will create a virtual environment and ask you which plugin to run.

For building the plugins for production, see the BUILD_PLUGINS.md file.

TODO: Do not forget to sign the plugins before uploading them to the store.


## 🔌 The Plugin System

Plugins are Object-Oriented modules that follow a strict structure for consistency and safety.

### Plugin Template Attributes

Every plugin defines the following core metadata:

| Property | Description |
| :--- | :--- |
| **Name** | Display name of the plugin (unique including translations). |
| **ID** | Unique identifier (e.g., `1234`). |
| **Version** | Version of the plugin. |
| **Order** | Menu placement priority (Dashboard: `0` < ... < Store: `100`). |
| **Description** | Brief explanation of capabilities. |
| **Icon** | Visual representation for the UI (light and dark mode). |
| **Translations** | Multilingual support for UI strings. |
| **Supported Systems** | OS compatibility (e.g., Windows, Linux, Mac). |
| |
| **Uninstall enabled** | Whether the plugin can be uninstalled by the user or is a system one (Dashboard, Store, Help and Settings). |

Each plugin must inherit from the `BasePlugin` class and implement the following methods:

| Function | Description |
| :--- | :--- |
| **init** | Initialize the plugin. Similarly to the above attributes, this function is called when the plugin is loaded and JSON list created. |
| **get_status** | Return the current operational state (OK, Info, Warning, Error, Critical). |
| **create_main_screen** | Creates the main screen of the plugin using CustomTkinter. |
| **README.md** | README.md file is required and it is used to display information about the plugin. |
| **create_settings_screen** | Creates the settings screen of the plugin using CustomTkinter (optional). |
| **get_call_list** | Returns a list of callable functions of the plugin (optional). |
| **create_CLI** | Creates the CLI interface of the plugin (optional). |
| **get_settings** | Returns the settings of the plugin (optional). |
| **set_settings** | Sets the settings of the plugin (optional). |


## 🚦 Dashboard & Status Indicators

The Dashboard provides a unified "You are protected" view. Each plugin reports its status using standardized icons:

| Icon | Status | Risk Level | Meaning |
| :---: | :--- | :--- | :--- |
| ⚛️ | **Critical** | Nuclear | Immediate action required. Significant threat or failure. |
| ⛔ | **Error** | High | Stopped or failed functionality. Stop/one-way sign. |
| ⚠️ | **Warning** | Medium | Attention needed or potential risk detected. |
| ✅ | **OK** | Low | System operational and healthy. |
| ℹ️ | **Info** | Unknown | No immediate risk, but action suggested to optimize safety. |

---


Each plugin should contain `main.py` and at least `README.md` file that explains how to use it, how to install it and a LICENSE file. In case the latter is missing, the Resistine GPL v2 license is applied.

Some plugins may also contain `settings.json` file that contains the settings of the plugin. This file is optional and is used to store the settings of the plugin.

Plugins that need to install something on the system should contain `install.sh` or `install.bat` file that contains the installation script. This file is optional and is used to install the plugin on the system. In case the files should be run as root, the `sudo` command should be used.


## 📄 License

The plugins may have their own licenses attached to them, but the Resistine Desktop App and most of the plugins created by Resistine are released under the GNU General Public License.

    Resistine AI EndPoint Detection and Response (AI EDR) for Windows, Mac and Linux Desktops
    Copyright (C) 2025 Resistine

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <https://www.gnu.org/licenses/>.
