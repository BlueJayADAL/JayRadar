"""
Output Package

This package contains classes that manage the final stage of the vision pipeline, controlling
how the processed data and frames are handled.

Modules:
    output: The base class for managing pipeline output. It defines the basic behavior for
            handling processed frames and data.
    nt_display: A class that displays the processed frames locally and sends the data to
                NetworkTables, allowing integration with other components in the system.
    nt_send: A class that sends the processed frame in a multiprocessing queue and also
             forwards the data to NetworkTables. This allows for efficient parallel
             processing of the data and frame handling.

Note:
    Users can create custom output implementations by subclassing the `Output` base class
    and defining their desired behavior for handling processed data and frames at the end
    of the vision pipeline.
"""  # noqa: E501

from .output import Output
from .nt_display import NTDisplay
from .nt_send import NTSend

__all__ = ['Output', 'NTDisplay', 'NTSend']
