
"""Wrapper for the Kokoro text-to-speech pipeline."""
import os
from numbers import Number
import torch
from kokoro import KPipeline
from storyboard.logger import logger
from storyboard.config import Config

class TTSPipeline:
    """Wrapper for the Kokoro text-to-speech pipeline."""

    def __init__(self, lang_code: str = 'a', num_threads: int = None):
        """
        Initializes the TTS pipeline.

        Args:
            lang_code (str, optional): The language code for the pipeline. Defaults to 'a'.
        """
        num_threads = int(os.environ.get('NUM_THREADS', num_threads or os.cpu_count() or 1))
        torch.set_num_threads(num_threads)
        self.pipeline = KPipeline(lang_code=lang_code)
        logger.info("Kokoro pipeline initialized.", num_threads=num_threads)

    def generate(self, text: str, voice: str = Config.DEFAULT_VOICE, speed: Number = Config.DEFAULT_SPEED, split_pattern: str = Config.DEFAULT_SPLIT_PATTERN):
        """Generates audio from text using the Kokoro pipeline.

        Args:
            text (str): The text to convert to speech.
            voice (str, optional): The voice to use. Defaults to Config.DEFAULT_VOICE.
            speed (Number, optional): The speed of the speech. Defaults to Config.DEFAULT_SPEED.
            split_pattern (str, optional): The pattern to split the text. Defaults to Config.DEFAULT_SPLIT_PATTERN.

        Yields:
            tuple: A tuple containing the generated group id, paragraph id, and audio.
        
        Raises:
            Exception: If an error occurs during audio generation.
        """
        try:
            yield from self.pipeline(text, voice=voice, speed=speed, split_pattern=split_pattern)
        except Exception as e:
            logger.error("Error generating sound with Kokoro.", error=str(e))
            raise
