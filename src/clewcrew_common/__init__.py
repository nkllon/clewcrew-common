"""
clewcrew-common

Your friendly neighborhood hallucination-busting task force.
This package provides common functionality used across all clewcrew components.
"""

__version__ = "0.1.0"
__author__ = "Lou Springer"
__email__ = "lou@example.com"

from .confidence import ConfidenceCalculator
from .logging import ClewcrewLogger
from .configuration import ConfigManager
from .data_models import BaseResult, BaseConfig
from .async_utils import AsyncExecutor
from .file_ops import FileOperations
from .validation import ValidationUtils

__all__ = [
    "ConfidenceCalculator",
    "ClewcrewLogger",
    "ConfigManager",
    "BaseResult",
    "BaseConfig",
    "AsyncExecutor",
    "FileOperations",
    "ValidationUtils",
]
