import os
from PIL import Image

class BasePlugin:
    def __init__(self, id, version, order, name, status, description, supported_systems, translations, icon_light_path, icon_dark_path, uninstall_enabled=True):
        """
        Initialize the BasePlugin with the given attributes.

        :param id: The unique identifier for the plugin.
        :param version: The version of the plugin.
        :param order: The order in which the plugin should be displayed.
        :param name: The name of the plugin.
        :param status: The current status of the plugin.
        :param description: A brief description of the plugin.
        :param supported_systems: A list of systems supported by the plugin.
        :param translations: A dictionary of translations for the plugin.
        :param icon_light_path: Path to the light mode icon.
        :param icon_dark_path: Path to the dark mode icon.
        :param uninstall_enabled: Whether the plugin can be uninstalled.
        """
        self.id = id
        self.version = version
        self.order = order
        self.name = name
        self.status = status
        self.description = description
        self.supported_systems = supported_systems
        self.translations = translations
        self.icon_light = icon_light_path
        self.icon_dark = icon_dark_path
        self.uninstall_enabled = uninstall_enabled
        self.icon = self.create_icon(size=(20, 20))
        self.icon_alert = None
        self.button = None
        self.app = None # Will be set by subclasses or manager

    def create_icon(self, size):
        """
        Mock icon creation for the test environment.
        """
        return None

    def get_status(self):
        return self.status
