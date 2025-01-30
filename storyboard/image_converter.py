
"""Handles image conversion to PNG format."""
import os
from typing import Optional
from PIL import Image
from storyboard.logger import logger


class ImageConverter:
    """Handles image conversion to PNG format."""

    @staticmethod
    def convert_to_png(local_image_path: str) -> Optional[str]:
        """Converts the image to PNG format.

        Args:
            local_image_path (str): The path to the image file.

        Returns:
             Optional[str]: The path to the converted PNG image file or None if error occurs.
        """
        if not local_image_path or not os.path.exists(local_image_path):
            logger.warning("Image not found for conversion.")
            return None
        try:
            image = Image.open(local_image_path)
            new_path = os.path.splitext(local_image_path)[0] + '.png'
            if os.path.exists(new_path):
                logger.info(f"Image already in PNG format: {new_path}")
                return new_path
            image.save(new_path, 'PNG')
            logger.info(f"Image converted to PNG: {new_path}")
            return new_path
        except Exception as e:
            logger.error(f"Error converting image {local_image_path} to PNG: {e}")
            return None
