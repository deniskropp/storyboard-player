
"""Represents a single scene in the storyboard."""
import os
from typing import Optional

from storyboard.config import Config
from storyboard.image_downloader import ImageDownloader
from storyboard.image_converter import ImageConverter
from storyboard.sound import Sound
from storyboard.pipeline import TTSPipeline
from storyboard.utils import FileUtils
from storyboard.logger import logger


class Scene:
    """Represents a single scene in the storyboard."""

    def __init__(self, description: str, image_url: Optional[str] = None, tts_pipeline: TTSPipeline = None):
        """
        Initializes a Scene object.

        Args:
            description (str): The description of the scene.
            image_url (Optional[str], optional): The URL of the image for the scene. Defaults to None.
            tts_pipeline (TTSPipeline, optional): The TTS pipeline to use. Defaults to a new TTSPipeline.
        """
        self.description = description
        self.image_url = image_url
        self.image_downloader = ImageDownloader(image_url=image_url)
        self.local_image_path: Optional[str] = None
        self.local_sound_path: Optional[str] = None
        self.tts_pipeline = tts_pipeline or TTSPipeline()
        self.initialize()

    def initialize(self) -> None:
        """Initializes the scene, downloading and converting images, and creating sound."""
        self.local_image_path = self.image_downloader.derive_local_file_name()
        self.image_downloader.local_image_path = self.local_image_path

        if self.image_url:
            self.image_downloader.download_image()
            if self.image_downloader.local_image_path:
                self.local_image_path = ImageConverter.convert_to_png(self.image_downloader.local_image_path)
                if not self.local_image_path:
                    logger.warning(f"Image conversion failed for scene description: {self.description}")
            else:
                logger.warning(f"Image download failed for scene description: {self.description}")

        self.local_sound_path = self.derive_local_sound_file_name()
        FileUtils.create_directory(os.path.dirname(self.local_sound_path))
        if not os.path.exists(self.local_sound_path):
            Sound(text=self.description, tts_pipeline=self.tts_pipeline).save(self.local_sound_path)

    def derive_local_sound_file_name(self) -> str:
        """Derives the local sound file name based on the image path, ensuring .wav extension.

        Returns:
            str: The local sound file path.
        """
        if self.local_image_path:
            file_name = os.path.splitext(os.path.basename(self.local_image_path))[0] + '.wav'
            return os.path.join(Config.SOUND_DIR, file_name)
        else:
            file_name = f"no_image_{hash(self.description)}.wav"
            return os.path.join(Config.SOUND_DIR, file_name)
