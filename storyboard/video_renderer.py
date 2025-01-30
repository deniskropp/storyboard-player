
"""Renders the storyboard scenes to a video."""
import os
import subprocess
import textwrap
from typing import List, Optional
from storyboard.config import Config
from storyboard.scene import Scene
from storyboard.utils import FileUtils
from storyboard.logger import logger

class VideoRenderer:
    """Renders the storyboard scenes to a video."""

    def __init__(self, scenes: List[Scene]):
        """
        Initializes the VideoRenderer.

        Args:
            scenes (List[Scene]): A list of Scene objects.
        """
        self.scenes = scenes

    def create_text_file(self, scene: Scene, index: int) -> str:
        """Creates a temporary text file for the scene description.

        Args:
            scene (Scene): The scene object.
            index (int): The index of the scene.

        Returns:
            str: The path to the temporary text file.
        """
        text_file = f"{Config.TEMP_TEXT_FILE_PREFIX}{index}.txt"
        try:
            with open(text_file, 'w', encoding='utf-8') as f:
                wrapped_text = textwrap.fill(scene.description, width=80)
                f.write(wrapped_text)
            return text_file
        except Exception as e:
            logger.error(f"Error creating text file for scene {index + 1}: {e}")
            return ""

    def create_video_segment(self, scene: Scene, index: int, temp_files: List[str]) -> Optional[str]:
        """Creates a video segment from a scene using FFmpeg.

        Args:
            scene (Scene): The scene object.
            index (int): The index of the scene.
            temp_files (List[str]): A list to keep track of temporary files.

        Returns:
             Optional[str]: The path to the generated video file, or None if an error occurred.
        """
        if not scene.local_image_path or not scene.local_sound_path:
            logger.warning(f"Skipping scene {index + 1}, no image or sound")
            return None

        text_file = self.create_text_file(scene, index)
        if not text_file:
            return None
        temp_files.append(text_file)
        video_file = f"{Config.TEMP_VIDEO_FILE_PREFIX}{index}.mp4"

        ffmpeg_command = [
            'ffmpeg',
            '-i', scene.local_image_path,
            '-i', scene.local_sound_path,
            '-vf', f"drawtext=textfile='{text_file}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-10",
            '-pix_fmt', 'yuv420p',
            '-y',  # Overwrite output files without asking
            video_file
        ]
        try:
            result = subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
            logger.info(f"Video segment created: {video_file}", stdout=result.stdout, stderr=result.stderr)
            temp_files.append(video_file)
            return video_file
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running FFmpeg for scene {index + 1}: {e}", stdout=e.stdout, stderr=e.stderr)
            return None

    def create_video_list_file(self, video_files: List[str], temp_files: List[str]) -> str:
        """Creates a temporary file listing the video segments for concatenation.

        Args:
            video_files (List[str]): A list of video file paths.
            temp_files (List[str]): A list to keep track of temporary files.

        Returns:
            str: The path to the list file.
        """
        list_file = Config.TEMP_LIST_FILE
        try:
            with open(list_file, 'w') as f:
                for file in video_files:
                    f.write(f"file '{file}'\n")
            temp_files.append(list_file)
            return list_file
        except Exception as e:
            logger.error(f"Error creating video list file: {e}")
            return ""

    def render_to_video(self, output_filename: str = Config.DEFAULT_OUTPUT_VIDEO) -> None:
        """Renders all scenes to a single video file.

        Args:
            output_filename (str, optional): The output video file name. Defaults to Config.DEFAULT_OUTPUT_VIDEO.
        """
        if not self.scenes:
            logger.warning("No scenes to render.")
            return
        temp_files: List[str] = []
        video_files: List[str] = []

        for i, scene in enumerate(self.scenes):
            video_file = self.create_video_segment(scene, i, temp_files)
            if video_file:
                video_files.append(video_file)

        if not video_files:
            logger.warning("No videos generated.")
            FileUtils.cleanup_files(temp_files)
            return

        list_file = self.create_video_list_file(video_files, temp_files)
        if not list_file:
            FileUtils.cleanup_files(temp_files)
            return
        
        ffmpeg_concat_command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            '-y',  # Overwrite output files without asking
            output_filename
        ]
        try:
            result = subprocess.run(ffmpeg_concat_command, check=True, capture_output=True, text=True)
            logger.info(f"Video rendered to {output_filename}", stdout=result.stdout, stderr=result.stderr)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during video concatenation: {e}", stdout=e.stdout, stderr=e.stderr)
        finally:
            FileUtils.cleanup_files(temp_files)
