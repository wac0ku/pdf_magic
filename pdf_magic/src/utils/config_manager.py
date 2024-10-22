import json
from .logger import logger

class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            logger.warning(f"Config file not foun f: {self.config_file_path}")
            return {}
        except Exception as e:
            logger.error(f"Error loading config from {self.config_file_path}: {str(e)}")
            raise

    def save_config(self, config):
        try:
            with open(self.config_file_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            logger.info(f"Config saved to {self.config_file_path}")
        except Exception as e:
            logger.error(f"Error saving config to {self.config_file_path}: {str(e)}")
            raise

    def get_config_value(self, key, default_value=None):
        return self.config.get(key, default_value)