"""
Handles the loading and saving of application settings, as well as providing default settings when necessary.
"""

from typing import Dict, TextIO
import os
import json

DEFAULT_SETTINGS_FILE = "settings/default_settings.json"


class SettingsManager:
    """
    Class for managing application settings.

    Methods
    -------
    default_settings() -> Dict[str, str]:
        Returns the default settings.
    load_settings(filename: str = DEFAULT_SETTINGS_FILE) -> Dict[str, str]:
        Loads settings from a JSON file.
    save_settings(settings, filename: str = DEFAULT_SETTINGS_FILE) -> None:
        Saves settings to a JSON file.
    load_settings_from_file(file: TextIO) -> Dict[str, str]:
        Loads settings from a file object.
    """

    def __init__(self):
        pass

    def default_settings(self) -> Dict[str, str]:
        """
        Returns the default settings.

        Returns
        -------
        Dict[str, str]
            Dictionary with default settings.
        """
        return {
            "folder_path": "",
            "target_extensions": "",
            "always_include": "",
            "excluded_dirs": "",
            "system_prompt": "",
        }

    def load_settings(self, filename: str = DEFAULT_SETTINGS_FILE) -> Dict[str, str]:
        """
        Loads settings from a JSON file.

        Parameters
        ----------
        filename : str, optional
            Name of the settings file. Default is DEFAULT_SETTINGS_FILE.

        Returns
        -------
        Dict[str, str]
            Dictionary with loaded settings or default settings if the file is not found.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.default_settings()

    def save_settings(self, settings, filename: str = DEFAULT_SETTINGS_FILE) -> None:
        """
        Saves settings to a JSON file.

        Parameters
        ----------
        settings : dict
            Dictionary with settings to save.
        filename : str, optional
            Name of the settings file. Default is DEFAULT_SETTINGS_FILE.
        """
        settings_dir = os.path.dirname(filename)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

    def load_settings_from_file(self, file: TextIO) -> Dict[str, str]:
        """
        Loads settings from a file object.

        Parameters
        ----------
        file : TextIO
            File object with settings in JSON format.

        Returns
        -------
        Dict[str, str]
            Dictionary with loaded settings or default settings if the file cannot be decoded.
        """
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return self.default_settings()
