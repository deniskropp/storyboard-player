
"""Generates QML file for displaying the storyboard."""
import os
from typing import List
from storyboard.config import Config
from storyboard.scene import Scene
from storyboard.logger import logger


class QMLGenerator:
    """Generates QML file for displaying the storyboard."""

    @staticmethod
    def generate_qml_scene_element(scene: Scene) -> str:
        """Generates a QML ListElement for a given scene.

        Args:
            scene (Scene): The scene object.

        Returns:
            str: The QML ListElement string.
        """
        return (
            '        ListElement {\n'
            f'            imagePath: "{os.path.abspath(scene.local_image_path)}"\n'
            f'            soundPath: "{os.path.abspath(scene.local_sound_path)}"\n'
            f'            description: "{scene.description}"\n'
            '        }\n'
        )

    @staticmethod
    def generate_qml_file(scenes: List[Scene], output_filename: str = Config.QML_OUTPUT_FILE) -> None:
        """Generates a QML file for displaying the storyboard with audio playback.

        Args:
            scenes (List[Scene]): A list of Scene objects.
            output_filename (str, optional): The output QML file name. Defaults to Config.QML_OUTPUT_FILE.
        """
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write('import QtQuick 2.15\n')
                f.write('import QtQuick.Window 2.15\n')
                f.write('import QtMultimedia 5.15\n\n')
                f.write('Window {\n')
                f.write('    width: 800\n')
                f.write('    height: 600\n')
                f.write('    visible: true\n')
                f.write('    title: qsTr("Storyboard")\n\n')
                f.write('    property int currentIndex: 0\n')
                f.write('    property var audioDurations: []\n\n')

                f.write('    ListModel {\n')
                f.write('        id: storyboardModel\n')
                for scene in scenes:
                    f.write(QMLGenerator.generate_qml_scene_element(scene))
                f.write('    }\n\n')

                f.write('    function initializeAudioDurations() {\n')
                for i, scene in enumerate(scenes):
                    f.write(f'        audio{i}.source = storyboardModel.get({i}).soundPath\n')
                f.write('    }\n\n')
                
                for i, scene in enumerate(scenes):
                    f.write(f'    Audio {{\n')
                    f.write(f'        id: audio{i}\n')
                    f.write(f'        source: ""\n')
                    f.write('        onLoaded: {{\n')
                    f.write(f'           audioDurations[{i}] = duration\n')
                    f.write('        }}\n')
                    f.write('    }\n\n')

                f.write('    ListView {\n')
                f.write('        anchors.fill: parent\n')
                f.write('        model: storyboardModel\n')
                f.write('        currentIndex: 0\n')
                f.write('        delegate: Rectangle {\n')
                f.write('            width: parent.width\n')
                f.write('            height: 400\n')
                f.write('            color: "lightgray"\n\n')
                f.write('            Image {\n')
                f.write('                id: sceneImage\n')
                f.write('                anchors.top: parent.top\n')
                f.write('                anchors.horizontalCenter: parent.horizontalCenter\n')
                f.write('                width: 300\n')
                f.write('                height: 200\n')
                f.write('                source: "file:///" + model.imagePath\n')
                f.write('                fillMode: Image.PreserveAspectFit\n')
                f.write('            }\n\n')
                f.write('            Text {\n')
                f.write('                id: sceneText\n')
                f.write('                anchors.top: sceneImage.bottom\n')
                f.write('                anchors.horizontalCenter: parent.horizontalCenter\n')
                f.write('                width: parent.width - 40\n')
                f.write('                wrapMode: Text.WordWrap\n')
                f.write('                text: model.description\n')
                f.write('            }\n')
                f.write('        }\n')
                f.write('    }\n\n')

                f.write('    Timer {\n')
                f.write('        id: sceneTimer\n')
                f.write('        interval: audioDurations[currentIndex]\n')
                f.write('        running: false\n')
                f.write('        repeat: true\n')
                f.write('        onTriggered: {\n')
                f.write('            if (currentIndex < storyboardModel.count - 1) {\n')
                f.write('                currentIndex++;\n')
                f.write('                sceneTimer.interval = audioDurations[currentIndex]\n')
                f.write('                playCurrentAudio();\n')
                f.write('            } else {\n')
                f.write('                currentIndex = 0; // Loop to the first scene\n')
                f.write('                sceneTimer.interval = audioDurations[currentIndex]\n')
                f.write('                playCurrentAudio();\n')
                f.write('            }\n')
                f.write('        }\n')
                f.write('    }\n\n')
                
                f.write('    function playCurrentAudio() {\n')
                f.write('        stopAllAudio();\n')
                f.write(f'        var currentAudio = "audio" + currentIndex\n')
                f.write('        if(Qt.getExistingObjects(currentAudio).length > 0) {\n')
                f.write('            Qt.getExistingObjects(currentAudio)[0].play();\n')
                f.write('        }\n')
                f.write('    }\n\n')
                
                f.write('    function stopAllAudio() {\n')
                for i in range(len(scenes)):
                    f.write(f'        audio{i}.stop();\n')
                f.write('    }\n\n')

                f.write('    Component.onCompleted: {\n')
                f.write('        initializeAudioDurations();\n')
                f.write('        sceneTimer.start();\n')
                f.write('        playCurrentAudio();\n')
                f.write('    }\n')
                f.write('}\n')

            logger.info(f"QML file generated: {output_filename}")
        except Exception as e:
            logger.error(f"Error generating QML file: {e}")
