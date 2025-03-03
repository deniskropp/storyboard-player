from setuptools import setup, find_packages

setup(
    name='storyboard-player',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'markdown',
        'Pillow',
        'requests',
        'soundfile',
        'FreeSimpleGUI',
        'kokoro',
        'ffmpeg-python'
    ],
    entry_points={
        'console_scripts': [
            'storyboard-player=main:main'
        ]
    },
    author='Denis Kropp',
    author_email='dok@directfb1.org',
    description='A tool to create and play storyboards with text-to-speech and video rendering.',
    url='https://github.com/deniskropp/storyboard-player',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
