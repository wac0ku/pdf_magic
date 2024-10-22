from PIL import Image
from .logger import logger

class ImageProcessor:
    @staticmethod
    def resize_image(image_path, output_path, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height))
            image.save(output_path)
            logger.info(f"Image resized and saved to {output_path}")
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise