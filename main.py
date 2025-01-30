
import argparse
import subprocess
from storyboard.config import Config
from storyboard.storyboard import Storyboard
from storyboard.logger import logger
from storyboard.qml_generator import QMLGenerator

def main():
    """Main function to parse arguments and run the storyboard processing."""
    parser = argparse.ArgumentParser(description='Process a storyboard file.')
    parser.add_argument('filename', help='The path to the storyboard markdown file.')
    parser.add_argument('--display', action='store_true', help='Display the storyboard in the console.')
    parser.add_argument('--display_gui', action='store_true', help='Display the storyboard in a GUI window.')
    parser.add_argument('--display_qml', action='store_true', help='Display the storyboard in a QML viewer.')
    parser.add_argument('--render_video', action='store_true', help='Render the storyboard to a video file.')
    parser.add_argument('--output', default=Config.DEFAULT_OUTPUT_VIDEO, help=f'The output video filename (default: {Config.DEFAULT_OUTPUT_VIDEO}).')
    parser.add_argument('--qml_output', default=Config.QML_OUTPUT_FILE, help=f'The output QML filename (default: {Config.QML_OUTPUT_FILE}).')

    args = parser.parse_args()
    storyboard = Storyboard(args.filename)

    if args.display:
        storyboard.display()
    if args.display_gui:
        storyboard.display_gui()
    if args.display_qml:
        QMLGenerator.generate_qml_file(storyboard.scenes, args.qml_output)
        try:
            subprocess.run(['qml', args.qml_output], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error displaying QML file: {e}")

    if args.render_video:
        storyboard.render_to_video(args.output)

if __name__ == "__main__":
    main()
