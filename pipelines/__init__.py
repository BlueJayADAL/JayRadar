"""
Vision Pipeline Package

This package allows users to create and manipulate vision pipelines. A pipeline is a static
sequence of processing steps that cannot be changed once created. The variable pipeline,
on the other hand, allows users to change settings while it runs, providing more flexibility.

Modules:
    pipeline: Defines the base class for static vision pipelines.
    variable_pipeline: Implements the variable pipeline that allows runtime changes.
    pipeline_manager: Provides a manager for creating and handling variable pipelines.
"""  # noqa: E501

from .pipeline import Pipeline
from .variable_pipeline import VariablePipeline
from .pipeline_manager import PipelineManager

__all__ = ['Pipeline', 'VariablePipeline', 'PipelineManager']
