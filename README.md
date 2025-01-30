# Storyboard Player 🎥

The Storyboard Player is a versatile tool designed to help creators visualize their storytelling ideas through the use of Markdown. Whether you're a filmmaker, game designer, or content creator, this tool streamlines the process of turning your storyboard concepts into actionable visual formats. With support for console display, graphical user interfaces, QML generation, and video rendering, the Storyboard Player enables a seamless storytelling workflow.

https://github.com/user-attachments/assets/95b40465-2464-4a57-ac59-146ae5d08689

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Displaying the Storyboard](#displaying-the-storyboard)
  - [Generating Files](#generating-files)
  - [Command Line Arguments](#command-line-arguments)
- [Configuration](#configuration)
- [Logging](#logging)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Display in Console**: Quickly view your storyboard's content directly in the terminal for easy debugging and review.
- **Display in GUI**: Visualize your storyboard in a user-friendly graphical interface, allowing for a more interactive experience.
- **Generate QML**: Create a QML file to display your storyboard in any QML viewer, making integration into other applications straightforward.
- **Render to Video**: Convert your storyboard into a video file, complete with images and text-to-speech audio, for easy sharing and presentation.

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - `markdown`
  - `FreeSimpleGUI`
  - `Pillow`
  - `requests`
  - `torch`
  - `kokoro`
  - `soundfile`
  - `subprocess`

## Installation

To install the Storyboard Player, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/deniskropp/storyboard-player.git
   ```
3. Navigate to the project directory:
   ```bash
   cd storyboard-player
   ```
4. Install the required dependencies:
   ```bash
   pip install markdown FreeSimpleGUI Pillow requests torch kokoro soundfile
   ```

## Usage

To use the Storyboard Player, you can run commands in your terminal. Here are some common functionalities:

### Displaying the Storyboard

- **In Console**:
  ```bash
  python main.py test/test-storyboard.md --display
  ```

- **In GUI**:
  ```bash
  python main.py test/test-storyboard.md --display_gui
  ```

### Generating Files

- **QML File**:
  ```bash
  python main.py test/test-storyboard.md --display_qml --qml_output my_player.qml
  ```
- **Render Video**:
  ```bash
  python main.py test/test-storyboard.md --render_video --output my_video.mp4
  ```

### Command Line Arguments

- `filename`: The path to the storyboard markdown file.
- `--display`: Display the storyboard in the console.
- `--display_gui`: Display the storyboard in a GUI window.
- `--display_qml`: Generate and display the storyboard in a QML viewer.
- `--render_video`: Render the storyboard to a video file.
- `--output`: The output video filename (default: `output.mp4`).
- `--qml_output`: The output QML filename (default: `storyboard.qml`).

Enjoy using the Storyboard Player!

## Configuration

Configuration constants for the storyboard player are defined in the `Config` class within the `storyboard/config.py` file. You can modify these constants to suit your needs.

## Logging

The application uses a custom logger defined in `storyboard/logger.py`. Logs are output to the console by default. You can also configure the logger to write logs to a file by uncommenting the relevant line in the `logger` initialization.

## Directory Structure

- `storyboard/`: Contains the main modules and classes.
- `images/`: Directory for downloaded images.
- `sound/`: Directory for generated sound files.
- `logs/`: Directory for log files (if logging to a file is enabled).

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the Storyboard Player.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Markdown](https://python-markdown.github.io/)
- [FreeSimpleGUI](https://pysimplegui.readthedocs.io/)
- [Pillow](https://pillow.readthedocs.io/)
- [Requests](https://docs.python-requests.org/)
- [Torch](https://pytorch.org/)
- [Kokoro](https://github.com/yourusername/kokoro)
- [Soundfile](https://pysoundfile.readthedocs.io/)
- [Subprocess](https://docs.python.org/3/library/subprocess.html)

## Contact

For any questions or inquiries, please contact the maintainer:

- **Name**: Denis O Kropp
- **Email**: dok@directfb1.org
- **GitHub**: [deniskropp](/deniskropp)

## Troubleshooting

| Issue                        | Solution                                                                  |
|------------------------------|---------------------------------------------------------------------------|
| FFmpeg Not Found             | Ensure that FFmpeg is installed and added to your system's PATH. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html). |
| Kokoro Installation Issues   | Ensure that Kokoro is installed correctly using pip: `pip install kokoro`. |
| Image Download Errors        | Verify that the image URLs in your storyboard file are correct and accessible. Check your internet connection and firewall settings. |
| Sound Generation Errors      | Ensure that the Kokoro library is properly installed and that the text-to-speech pipeline is initialized correctly. |

### Debugging Tips

- Enable debug logging by setting the logging level to `DEBUG` in the `Logger` class.
- Check the console output for any error messages or warnings.
- Review the log files (if logging to a file is enabled) for more detailed information.

**Happy coding!**

## Changelog

### Version 1.0.0 (Initial Release)

- Added support for displaying storyboard in the console.
- Added support for displaying storyboard in a GUI window.
- Added support for generating QML files.
- Added support for rendering storyboard to a video file.
- Implemented image downloading and conversion.
- Implemented text-to-speech generation and audio file saving.
- Added configuration constants and logging functionality.
- Created a comprehensive README with usage instructions and troubleshooting tips.

## Roadmap

### Future Features

- **Improved GUI**: Enhance the GUI with more interactive elements and better user experience.
- **Additional Export Formats**: Support exporting storyboard to other formats such as HTML, PDF, etc.
- **Enhanced TTS**: Improve text-to-speech quality and add support for more languages.
- **Cloud Integration**: Integrate cloud services for image storage and TTS processing.
- **User Authentication**: Add user authentication for personalized storyboard management.

Stay tuned for updates and new features!

## Contributing Guidelines

### How to Contribute

1. **Fork the Repository**: Create a fork of the repository on GitHub.
2. **Clone the Fork**: Clone your fork to your local machine.
   ```bash
   git clone https://github.com/yourusername/storyboard-player.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Make your changes and commit them.
   ```bash
   git commit -m "Add your commit message here"
   ```
5. **Push Changes**: Push your changes to your fork.
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**: Open a pull request to the main repository.

### Testing

- Ensure that your changes do not break existing functionality.
- Write unit tests for new features if applicable.

Thank you for your contributions to the Storyboard Playe
