import os
import shutil
from .logger import logger

class FileHandler:
    @staticmethod
    def create_directory(path):
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created: {path}")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {str(e)}")
            raise

    @staticmethod
    def delete_file(path):
        try:
            os.remove(path)
            logger.info(f"File deleted: {path}")
        except Exception as e:
            logger.error(f"Error deleting file {path}: {str(e)}")
            raise

    @staticmethod
    def move_file(src, dst):
        try:
            shutil.move(src, dst)
            logger.info(f"File moved from {src} to {dst}")
        except Exception as e:
            logger.error(f"Error moving file from {src} to {dst}: {str(e)}")
            raise

    @staticmethod
    def copy_file(src, dst):
        try:
            shutil.copy2(src, dst)
            logger.info(f"File copied from {src} to {dst}")
        except Exception as e:
            logger.error(f"Error copying file from {src} to {dst}: {str(e)}")
            raise

    @staticmethod
    def get_file_size(path):
        try:
            return os.path.getsize(path)
        except Exception as e:
            logger.error(f"Error getting file size for {path}: {str(e)}")
            raise