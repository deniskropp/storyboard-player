
"""Handles text-to-speech generation and audio file saving."""
from numbers import Number
import soundfile as sf
from storyboard.config import Config
from storyboard.pipeline import TTSPipeline
from storyboard.logger import logger


class Sound:
    """Handles text-to-speech generation and audio file saving."""

    def __init__(self, text: str, voice: str = Config.DEFAULT_VOICE, speed: Number = Config.DEFAULT_SPEED, split_pattern: str = Config.DEFAULT_SPLIT_PATTERN, tts_pipeline: TTSPipeline = None):
        """
        Initializes a Sound object.

        Args:
            text (str): The text to convert to speech.
            voice (str, optional): The voice to use. Defaults to Config.DEFAULT_VOICE.
            speed (Number, optional): The speed of the speech. Defaults to Config.DEFAULT_SPEED.
            split_pattern (str, optional): The pattern to split the text. Defaults to Config.DEFAULT_SPLIT_PATTERN.
            tts_pipeline (TTSPipeline, optional): The TTS pipeline to use. Defaults to a new TTSPipeline.
        """
        self.text = text
        self.voice = voice
        self.speed = speed
        self.split_pattern = split_pattern
        self.tts_pipeline = tts_pipeline or TTSPipeline()
        self.generator = self.tts_pipeline.generate(text, voice=voice, speed=speed, split_pattern=split_pattern)

    def __iter__(self):
        """Returns the iterator object."""
        return self

    def __next__(self):
         """Gets the next audio chunk from the generator."""
         try:
             gs, ps, audio = next(self.generator)
             return gs, ps, audio
         except StopIteration:
            raise
         

    def save(self, output_file: str) -> None:
        """Saves the generated audio to a WAV file.

        Args:
            output_file (str): The path to save the audio file.
        """
        try:
            with sf.SoundFile(output_file, 'w', 24000, 1) as f:
                for _, _, audio in self:
                    f.write(audio)
            logger.info(f"Audio saved to {output_file}")
        except sf.LibsndfileError as e:
            logger.error(f"Error saving audio file {output_file}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving audio: {e}")
            raise
