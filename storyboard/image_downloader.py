
"""Handles image downloading and processing."""
import os
from typing import Optional
from urllib.parse import urlparse
import requests
from storyboard.config import Config
from storyboard.logger import logger
from storyboard.utils import FileUtils


class ImageDownloader:
    """Handles image downloading and processing."""

    def __init__(self, image_url: Optional[str] = None):
        """
        Initializes the ImageDownloader.

        Args:
            image_url (Optional[str], optional): The URL of the image. Defaults to None.
        """
        self.image_url = image_url
        self.local_image_path: Optional[str] = None

    def derive_local_file_name(self) -> Optional[str]:
        """Derives the local file name from the image URL.

        Returns:
             Optional[str]: The local file path or None if URL is not set or error occurs.
        """
        if not self.image_url:
            logger.warning("Image URL is not set.")
            return None
        try:
            parsed_url = urlparse(self.image_url)
            file_name = os.path.basename(parsed_url.path)
            return os.path.join(Config.IMAGES_DIR, file_name)
        except Exception as e:
            logger.error(f"Error deriving local file name: {e}")
            return None

    def download_image(self) -> None:
        """Downloads the image from the URL if it doesn't exist locally."""
        if not self.image_url:
            logger.warning("Image URL is not set. Skipping download.")
            return

        if self.local_image_path and os.path.exists(self.local_image_path):
            logger.info(f"Image already exists locally: {self.local_image_path}")
            return

        if not self.local_image_path:
            logger.error("Local image path not set.")
            return

        FileUtils.create_directory(os.path.dirname(self.local_image_path))

        try:
            response = requests.get(self.image_url, stream=True)
            response.raise_for_status()
            with open(self.local_image_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logger.info(f"Image downloaded to {self.local_image_path}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image from {self.image_url}: {e}")
            self.local_image_path = None
