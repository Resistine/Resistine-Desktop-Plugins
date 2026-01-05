import customtkinter
import os
import sys
import importlib

# Ensure we can import from the root directory
base_dir = os.path.dirname(os.path.realpath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

def discover_plugins(plugins_dir):
    """
    Search for subdirectories in plugins/ that contain a main.py file.
    """
    plugins = []
    if not os.path.exists(plugins_dir):
        return plugins
    
    for item in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, item)
        if os.path.isdir(plugin_path) and not item.startswith('_') and not item.startswith('.'):
            if os.path.exists(os.path.join(plugin_path, 'main.py')):
                plugins.append(item)
    return sorted(plugins)

def select_plugin(plugins):
    """
    Prompt the user to select a plugin from the list.
    """
    if not plugins:
        print("No plugins found in the plugins/ directory.")
        return None
    
    print("\n--- Available Plugins ---")
    for i, name in enumerate(plugins, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = input(f"\nSelect a plugin to run (1-{len(plugins)}) [default: 1]: ").strip()
            if choice == "":
                return plugins[0]
            idx = int(choice) - 1
            if 0 <= idx < len(plugins):
                return plugins[idx]
            else:
                print(f"Please enter a number between 1 and {len(plugins)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

class TestApp(customtkinter.CTk):
    def __init__(self, plugin_module_name):
        super().__init__()

        self.title(f"Resistine Plugin Test Runner - {plugin_module_name}")
        self.geometry("1000x800")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Dynamically import the plugin
        try:
            print(f"Loading plugin: {plugin_module_name}...")
            module = importlib.import_module(f"plugins.{plugin_module_name}.main")
            PluginClass = getattr(module, 'Plugin')
            self.plugin = PluginClass(self)
        except Exception as e:
            print(f"Error loading plugin {plugin_module_name}: {e}")
            sys.exit(1)
        
        # Initialize UI
        if hasattr(self.plugin, 'create_main_screen'):
            self.plugin.create_main_screen()
            
            # Grid the plugin's main frame if it was created
            if hasattr(self.plugin, 'main_frame'):
                self.plugin.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            else:
                print("Warning: Plugin.create_main_screen() did not set self.main_frame.")
        else:
            print("Error: Plugin does not implement create_main_screen()")

if __name__ == "__main__":
    # 1. Discover plugins
    plugins_dir = os.path.join(base_dir, 'plugins')
    available_plugins = discover_plugins(plugins_dir)
    
    # 2. Ask user for selection
    selected = select_plugin(available_plugins)
    
    if selected:
        # 3. Start UI
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        
        app = TestApp(selected)
        print(f"Starting test window for '{selected}'...")
        app.mainloop()
