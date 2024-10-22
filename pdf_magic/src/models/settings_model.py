import json
from PyQt5.QtCore import QObject, pyqtSignal
import os

class SettingsModel(QObject):
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._settings = {
            'default_output_directory': '',
            'default_conversion_type': 'PDF_TO_DOCX',
            'max_concurrent_conversions': 2,
            'overwrite_existing_files': False,
            'use_ocr_for_text_extraction': True
        }
        self._settings_file = 'config/settings.json'
        self.load_settings()

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        if self._settings.get(key) != value:
            self._settings[key] = value
            self.settings_changed.emit()
            self.save_settings()

    def load_settings(self):
        if os.path.exists(self._settings_file):
            try:
                with open(self._settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self._settings.update(loaded_settings)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self._settings_file}")
            except IOError:
                print(f"Error reading file {self._settings_file}")

    def save_settings(self):
        os.makedirs(os.path.dirname(self._settings_file), exist_ok=True)
        try:
            with open(self._settings_file, 'w') as f:
                json.dump(self._settings, f, indent=4)
        except IOError:
            print(f"Error writing to file {self._settings_file}")

    def reset_to_defaults(self):
        self._settings = {
            'default_output_directory': '',
            'default_conversion_type': 'PDF_TO_DOCX',
            'max_concurrent_conversions': 2,
            'overwrite_existing_files': False,
            'use_ocr_for_text_extraction': True
        }
        self.settings_changed.emit()
        self.save_settings()