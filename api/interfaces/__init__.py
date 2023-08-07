"""
Interfaces Package

This package contains classes that provide various user interfaces for interacting with the
vision pipeline and displaying processed frames.

Modules:
    cv2_ui: An interface that displays the frame using OpenCV's HighGUI and allows users to
            interact with the pipeline using keypresses. It provides real-time feedback for
            pipeline tuning.
    terminal_ui: An interface that displays the frame in a pop-up terminal window and allows
                 users to interact with the pipeline through terminal prompts. It enables
                 straightforward pipeline adjustments via command-line inputs.
    web_ui: An interface that streams the video frame to a webpage and allows users to interact
            with the pipeline through the webpage's UI. It provides a web-based platform for
            fine-tuning the vision pipeline.

Note:
    Users can choose the appropriate interface based on their preferred mode of interaction
    with the vision pipeline. Each interface offers unique features and benefits for pipeline
    adjustment and optimization.
"""  # noqa: E501

from .react_ui import ReactUI
from .terminal_ui import TerminalUI
from .cv2_ui import CV2UI

__all__ = ['TerminalUI', 'CV2UI', 'ReactUI']
