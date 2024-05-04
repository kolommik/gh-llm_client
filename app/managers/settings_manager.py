import json


class SettingsManager:
    def __init__(self, filename="settings/settings.json"):
        self.filename = filename

    def load_settings(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.default_settings()

    def save_settings(self, settings):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

    def default_settings(self):
        return {
            "folder_path": "",
            "target_extensions": "",
            "always_include": "",
            "excluded_dirs": "",
            "system_prompt": "",
        }
