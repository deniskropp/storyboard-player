# Storyboard Player 🎥

The Storyboard Player is a versatile tool designed to help creators visualize their storytelling ideas through the use of Markdown. Whether you're a filmmaker, game designer, or content creator, this tool streamlines the process of turning your storyboard concepts into actionable visual formats. With support for console display, graphical user interfaces, QML generation, and video rendering, the Storyboard Player enables a seamless storytelling workflow.

https://github.com/user-attachments/assets/95b40465-2464-4a57-ac59-146ae5d08689

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Displaying the Storyboard](#displaying-the-storyboard)
  - [Generating Files](#generating-files)
  - [Command Line Arguments](#command-line-arguments)

## Features

- **Markdown Parsing**: Convert markdown files into storyboard scenes.
- **Image Handling**: Download and convert images to PNG format.
- **Text-to-Speech**: Generate audio from scene descriptions using the Kokoro TTS pipeline.
- **Video Rendering**: Render scenes into a single video file.
- **GUI Display**: Display storyboard scenes in a GUI window.
- **QML Display**: Generate and display a QML file for interactive storyboard playback.

## Installation

    ```bash
        pip install storyboard-player
    ```

## Usage

To use the Storyboard Player, you can run commands in your terminal. Here are some common functionalities:

### Displaying the Storyboard

**In Console**:

    ```bash
        storyboard-player test/test-storyboard.md --display
    ```

**In GUI**:

    ```bash
        storyboard-player test/test-storyboard.md --display_gui
    ```

### Generating Files

**QML File**:

    ```bash
        storyboard-player test/test-storyboard.md --display_qml --qml_output my_player.qml
    ```

**Render Video**:

    ```bash
        storyboard-player test/test-storyboard.md --render_video --output my_video.mp4
    ```

### Command Line Arguments

- `filename`: The path to the storyboard markdown file.
- `--display`: Display the storyboard in the console.
- `--display_gui`: Display the storyboard in a GUI window.
- `--display_qml`: Generate and display the storyboard in a QML viewer.
- `--render_video`: Render the storyboard to a video file.
- `--output`: The output video filename (default: `output.mp4`).
- `--qml_output`: The output QML filename (default: `storyboard.qml`).

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the Storyboard Player.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
