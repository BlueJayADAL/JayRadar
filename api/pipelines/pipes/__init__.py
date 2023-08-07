"""
Pipes Package

This sub-package contains classes representing different stages in the vision pipeline. Each pipe
performs specific transformations on input images to prepare them for further processing.

Modules:
    pipe: The base class for vision pipeline stages. It does not perform any transformation
          and serves as the starting point for custom pipe implementations.
    hsv_pipe: A pipe that controls the saturation, contrast, and brightness of images. It
              enhances color characteristics for better feature extraction.
    rgb_pipe: A pipe that controls the red, green, and blue balance of images. It allows users
              to adjust color channels to correct color imbalances.
    yolov8_pipe: A pipe that runs input images through the YOLOv8 object detection model and
                 extracts data about detected objects. It enriches the pipeline with object
                 detection capabilities.

Note:
    Users can create custom pipe implementations by subclassing the `Pipe` base class and
    implementing their specific transformations according to their pipeline requirements.
"""  # noqa: E501

from .pipe import Pipe
from .hsv_pipe import HSVPipe
from .rgb_pipe import RGBPipe
from .yolov8_pipe import YOLOv8Pipe

__all__ = ['Pipe', 'HSVPipe', 'RGBPipe', 'YOLOv8Pipe']
