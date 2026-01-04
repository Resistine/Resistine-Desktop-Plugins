# @file plugins/template/main.py
"""
This module contains the main functionality for the Template plugin.
This serves as a starting point for creating new plugins.
Author: Petr and the Resistine Team
Copyright (c) Resistine 2026
Licensed under the GNU General Public License v2 or later
"""

import os
import customtkinter
from plugins.base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    @brief Plugin class for the Template plugin.
    """

    def __init__(self, app):
        """
        @brief Initialize the Template plugin.
        :param app: Main application object.
        """
        super().__init__(
            id="000", # ID of the plugin is given by Resistine (expect something like 1234)
            version="2026.01.04-alpha", # Version of the plugin
            order=7, # Order of the plugin
            name="Template", # Name of the plugin
            description="A template plugin to demonstrate plugin structure.", # Description of the plugin
            supported_systems=["Windows", "Linux", "Mac"], # Supported systems
            translations={"US": "Template", "DE": "Template", "ES": "Plantilla", "FR": "Modèle"},
            icon_light_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "template_light.png"
            ),
            icon_dark_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "template_dark.png"
            )
        )
        self.app = app

    def create_main_screen(self):
        """
        @brief Create the main screen for the Template plugin.
        """
        self.main_frame = customtkinter.CTkFrame(
            self.app, corner_radius=0, fg_color="transparent"
        )
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self.main_frame,
            text="Hello World from the Template Plugin!",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label.grid(row=0, column=0, padx=20, pady=20)

        return self.main_frame
