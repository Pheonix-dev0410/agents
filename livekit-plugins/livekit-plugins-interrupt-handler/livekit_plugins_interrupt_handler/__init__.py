"""
LiveKit Intelligent Interruption Handler Plugin
Filters filler-word interruptions while maintaining natural conversation flow.
"""

from .config import InterruptionConfig
from .handler import InterruptionHandler

__version__ = "0.1.0"

__all__ = [
    "InterruptionHandler",
    "InterruptionConfig",
]
