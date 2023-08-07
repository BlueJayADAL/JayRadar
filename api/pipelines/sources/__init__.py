"""
Source Package

This sub-package contains classes that provide access to various sources for vision pipelines.
A source is a component that captures images or video frames and makes them available
for processing by vision pipelines.

Modules:
    base_source: Defines the base class for accessing camera sources using OpenCV.
    threaded_source: Implements a threaded source that continuously grabs frames
                     from a web camera and displays them on demand.
"""  # noqa: E501

from .source import Source
from .threaded_source import ThreadedSource

__all__ = ['Source', 'ThreadedSource']
