"""
Handles the loading and saving of application settings, as well as providing default settings when necessary.
"""

from typing import Dict, TextIO
import os
import json

DEFAULT_SETTINGS_FILE = "settings/default_settings.json"


class SettingsManager:
    def __init__(self):
        pass

    def default_settings(self) -> Dict[str, str]:
        return {
            "folder_path": "",
            "target_extensions": "",
            "always_include": "",
            "excluded_dirs": "",
            "system_prompt": "",
        }

    def load_settings(self, filename: str = DEFAULT_SETTINGS_FILE) -> Dict[str, str]:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.default_settings()

    def save_settings(self, settings, filename: str = DEFAULT_SETTINGS_FILE) -> None:
        settings_dir = os.path.dirname(filename)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

    def load_settings_from_file(self, file: TextIO) -> Dict[str, str]:
        """Load settings from a file-like object."""
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return self.default_settings()
