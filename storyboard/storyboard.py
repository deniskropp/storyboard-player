
"""Manages the storyboard, including parsing, displaying, and rendering."""
import re
import textwrap
from typing import List, Optional
import markdown
import FreeSimpleGUI as sg
from storyboard.config import Config
from storyboard.scene import Scene
from storyboard.video_renderer import VideoRenderer
from storyboard.logger import logger
from storyboard.pipeline import TTSPipeline
from storyboard.qml_generator import QMLGenerator
import subprocess


class Storyboard:
    """Manages the storyboard, including parsing, displaying, and rendering."""

    def __init__(self, filename: str, tts_pipeline: TTSPipeline = None):
        """
        Initializes a Storyboard object.

        Args:
            filename (str): The path to the storyboard markdown file.
             tts_pipeline (TTSPipeline, optional): The TTS pipeline to use. Defaults to a new TTSPipeline.
        """
        self.filename = filename
        self.scenes: List[Scene] = []
        self.title: str = "Unknown Storyboard"
        self.tts_pipeline = tts_pipeline or TTSPipeline()
        self.parse_markdown()

    def parse_markdown(self) -> None:
        """Parses the markdown file to extract the title and scenes."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
        except Exception as e:
            logger.error(f"Error reading markdown file: {e}")
            return

        html = markdown.markdown(markdown_content)
        self.extract_title(html)
        self.extract_scenes(html)

    def extract_title(self, html: str) -> None:
        """Extracts the title from the HTML content."""
        title_pattern = re.compile(r'<h.>(.*?)</h.>')
        title_match = title_pattern.search(html)
        if title_match:
            self.title = title_match.group(1)
            logger.info(f"Title extracted: {self.title}")

    def extract_scenes(self, html: str) -> None:
        """Extracts scenes from the HTML content."""
        scene_pattern = re.compile(r'<img.*?src="(.*?)".*?>.*?<p>(.*?)</p>', re.DOTALL)
        matches = scene_pattern.findall(html)

        for image_url, description in matches:
            cleaned_description = re.sub(r' \(.*?\)', '', description).strip()
            try:
                self.add_scene(Scene(cleaned_description, image_url, tts_pipeline=self.tts_pipeline))
            except Exception as e:
                logger.error(f"Error creating scene: {e}")

    def add_scene(self, scene: Scene) -> None:
        """Adds a scene to the storyboard."""
        self.scenes.append(scene)
        logger.info(f"Scene added: {scene.description}")

    def display(self) -> None:
        """Displays the storyboard content in the console."""
        print(f"Title: {self.title}\n")
        for i, scene in enumerate(self.scenes):
            print(f"\n### Scene {i + 1}")
            if scene.local_image_path:
                print(f"Image File: {scene.local_image_path}")
            else:
                print("No image available\n")
            if scene.local_sound_path:
                print(f"Sound File: {scene.local_sound_path}")
            else:
                print("No sound available\n")
            print(scene.description)

    def display_gui(self) -> None:
        """Displays the storyboard content in a GUI window."""
        layout = []
        layout.append([sg.Text(self.title, font=('Calibri', 20))])
        image = sg.Image()
        text = sg.Text(font=('Calibri', 20))
        layout.append([image])
        layout.append([text])

        window = sg.Window('Storyboard', layout, finalize=True)

        for scene in self.scenes:
            if scene.local_image_path:
                try:
                    image.update(filename=scene.local_image_path)
                except Exception as e:
                    logger.error(f"Error loading image {scene.local_image_path}: {e}")
                    layout.append([sg.Text(f"Error loading image: {e}")])
            else:
                layout.append([sg.Text("No image available")])

            wrapped_text = textwrap.fill(scene.description, width=170)
            text.update(wrapped_text)

            event, _ = window.read(timeout=5000)
            if event == sg.WIN_CLOSED:
                break
        window.close()

    def render_to_video(self, output_filename: str = Config.DEFAULT_OUTPUT_VIDEO) -> None:
        """Renders the storyboard to a video file."""
        renderer = VideoRenderer(self.scenes)
        renderer.render_to_video(output_filename)
