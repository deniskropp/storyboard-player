
"""Utility functions for file and directory operations."""
import os
import soundfile as sf
from typing import List
from storyboard.logger import logger

class FileUtils:
    """Utility functions for file and directory operations."""

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """Creates a directory if it doesn't exist.

        Args:
            directory_path (str): The path to the directory.
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            logger.info(f"Directory created: {directory_path}")
        except OSError as e:
            logger.error(f"Error creating directory {directory_path}: {e}")

    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """Gets the duration of an audio file in seconds.

        Args:
            file_path (str): The path to the audio file.

        Returns:
            float: The duration of the audio file in seconds, or 0.0 if an error occurred.
        """
        try:
            with sf.SoundFile(file_path) as f:
                duration = len(f) / f.samplerate
                return duration
        except sf.LibsndfileError as e:
            logger.error(f"Error reading audio file {file_path}: {e}")
            return 0.0
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting audio duration: {e}")
            return 0.0

    @staticmethod
    def cleanup_files(temp_files: List[str]) -> None:
        """Cleans up temporary files.

        Args:
            temp_files (List[str]): A list of file paths to remove.
        """
        for file in temp_files:
            try:
                os.remove(file)
                logger.info(f"Temporary file removed: {file}")
            except Exception as e:
                logger.error(f"Error deleting file {file}: {e}")
