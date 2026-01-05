#!/usr/bin/env python3
"""
Plugin Build Script
Generates plugins.json by parsing plugin source code using AST.
Does not require plugin dependencies to be installed.
"""

import ast
import json
import os
import argparse
import sys
import zipfile
import shutil
import fnmatch
from datetime import datetime

def parse_plugin_file(file_path):
    """
    Parse a plugin's main.py file to extract metadata from the Plugin class.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    metadata = {}

    class PluginVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node):
            if node.name == 'Plugin':
                # Found the Plugin class, look for __init__
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                        self.process_init(item)

        def process_init(self, node):
            # Look for super().__init__(...) call
            for stmt in node.body:
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    # Check if it calls super().__init__
                    if (isinstance(func, ast.Attribute) and func.attr == '__init__' 
                        and isinstance(func.value, ast.Call) and isinstance(func.value.func, ast.Name) 
                        and func.value.func.id == 'super'):
                        
                        self.extract_kwargs(stmt.value)

        def extract_kwargs(self, call_node):
            for keyword in call_node.keywords:
                arg_name = keyword.arg
                value_node = keyword.value
                
                try:
                    val = self.get_literal_value(value_node)
                    if arg_name == 'icon_light_path' or arg_name == 'icon_dark_path':
                        # Special handling for paths: assume os.path.join(..., "filename.png")
                        # We just want the filename
                        val = self.extract_filename_from_path(value_node)
                        # Rename keys to match JSON schema
                        arg_name = 'icon_light' if arg_name == 'icon_light_path' else 'icon_dark'
                    
                    if val is not None:
                        metadata[arg_name] = val
                except Exception as e:
                    print(f"Warning: could not extract value for {arg_name}: {e}")

        def get_literal_value(self, node):
            # Safe literal extraction
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.List):
                return [self.get_literal_value(elt) for elt in node.elts]
            elif isinstance(node, ast.Dict):
                return {self.get_literal_value(k): self.get_literal_value(v) for k, v in zip(node.keys, node.values)}
            return None

        def extract_filename_from_path(self, node):
            # Try to handle os.path.join(..., "filename") patterns
            if isinstance(node, ast.Call):
                # Check args for string literals
                for arg in node.args:
                    val = self.get_literal_value(arg)
                    if isinstance(val, str) and (val.endswith('.png') or val.endswith('.svg') or val.endswith('.ico')):
                        return val
            # Fallback if it's just a string
            val = self.get_literal_value(node)
            if isinstance(val, str):
                return os.path.basename(val)
            return None

    PluginVisitor().visit(tree)
    return metadata

def create_plugin_archive(plugin_dir, output_path):
    """
    Create a zip archive of the plugin directory.
    Excludes files and directories based on root .gitignore and common patterns.
    """
    # Load .gitignore patterns from root
    root_dir = os.path.dirname(os.path.realpath(__file__))
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove trailing slash for matching consistency
                    patterns.append(line.rstrip('/'))
    
    # Always exclude these for safety
    patterns.extend(['__pycache__', '.git', '.vscode', '.venv', '*.py[codz]', '*.zip'])

    def should_ignore(path, name):
        # Check against patterns
        # Note: This is a simplified .gitignore matcher
        for pattern in patterns:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path, pattern):
                return True
        return False

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(plugin_dir):
                # Calculate path relative to plugin root for pattern matching
                rel_root = os.path.relpath(root, plugin_dir)
                if rel_root == '.':
                    rel_root = ''

                # Modify dirs in-place to skip ignored directories
                ignored_dirs = [d for d in dirs if should_ignore(os.path.join(rel_root, d), d)]
                for d in ignored_dirs:
                    dirs.remove(d)
                
                for file in files:
                    rel_file_path = os.path.join(rel_root, file)
                    if should_ignore(rel_file_path, file):
                        continue
                        
                    file_path = os.path.join(root, file)
                    # Archive name should be relative to the plugin root
                    zipf.write(file_path, rel_file_path)
        return True
    except Exception as e:
        print(f"Error creating archive for {plugin_dir}: {e}")
        return False

def build_plugins_json(plugins_dir, output_file, version, url_base=None, downloads_dir=None):
    if not os.path.exists(plugins_dir):
        print(f"Error: Directory {plugins_dir} does not exist.")
        sys.exit(1)

    if downloads_dir:
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
            print(f"Created downloads directory: {downloads_dir}")

    plugins_list = []
    
    # Iterate over direct subdirectories
    for item in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, item)
        if not os.path.isdir(plugin_path) or item.startswith('_') or item.startswith('.'):
            continue

        main_py = os.path.join(plugin_path, 'main.py')
        if not os.path.exists(main_py):
            continue

        print(f"Processing plugin: {item}...")
        meta = parse_plugin_file(main_py)
        
        if meta:
            # Add version if missing (inherit global version or default)
            if 'version' not in meta:
                meta['version'] = version
           
            # ID-based uninstall disabling:
            # 001: Dashboard, 004: Store, 009: Help, 010: Settings
            disabled_uninstall_ids = ["001", "004", "009", "010"]
            if 'id' in meta and meta['id'] in disabled_uninstall_ids:
                meta['uninstall_enabled'] = False
            else:
                meta['uninstall_enabled'] = True

            # Enforcement: Check for README.md
            readme_path = os.path.join(plugin_path, 'README.md')
            has_readme = os.path.exists(readme_path)
            if not has_readme:
                print(f"Error: Plugin {item} is missing README.md. Documentation is required.")

            # License handling: Copy root LICENSE.md if missing
            license_files = ['LICENSE', 'LICENSE.md']
            has_license = any(os.path.exists(os.path.join(plugin_path, f)) for f in license_files)
            if not has_license:
                root_license = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LICENSE.md')
                if os.path.exists(root_license):
                    dest_license = os.path.join(plugin_path, 'LICENSE.md')
                    shutil.copy2(root_license, dest_license)
                    print(f"  -> Copied root LICENSE.md to {item}")
                else:
                    print(f"Warning: Root LICENSE.md not found, could not copy to {item}")

            # Zip packing and URL generation
            if downloads_dir:
                if not has_readme:
                    print(f"  -> Skipping archive creation for {item} due to missing README.md")
                else:
                    zip_filename = f"{item.lower()}.zip"
                    zip_path = os.path.join(downloads_dir, zip_filename)
                    
                    if create_plugin_archive(plugin_path, zip_path):
                        print(f"  -> Created archive: {zip_filename}")
                        
                        if url_base:
                            # Ensure url_base doesn't end with slash if we add one, or handle cleaner
                            base = url_base.rstrip('/')
                            meta['url'] = f"{base}/{zip_filename}"
                    else:
                        print(f"  -> Failed to create archive for {item}")

            plugins_list.append(meta)
        else:
            print(f"Failed to extract metadata for {item}")

    # Sort by order (primary) and name (secondary)
    plugins_list.sort(key=lambda x: (x.get('order', 99), x.get('name', '').lower()))

    output = {
        "version": version,
        "plugins": plugins_list
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"Successfully wrote {len(plugins_list)} plugins to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build plugins.json from source.')
    parser.add_argument('--plugins-dir', default='./plugins', help='Path to plugins directory')
    parser.add_argument('--output', default='plugins.json', help='Output JSON file')
    parser.add_argument('--version', default=datetime.now().strftime('%Y.%m.%d-alpha'), help='Version string')
    parser.add_argument('--url-base', help='Base URL for plugin downloads')
    parser.add_argument('--downloads-dir', help='Directory to save plugin zip archives')

    args = parser.parse_args()
    
    build_plugins_json(args.plugins_dir, args.output, args.version, args.url_base, args.downloads_dir)
