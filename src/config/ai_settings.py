"""
AI Configuration Settings

This module centralizes all configurable AI parameters used
throughout the application.

Future AI models should import settings from here rather than
using hard-coded values.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AISettings:
    """
    Global AI configuration.
    """

    # Default AI model
    DEFAULT_MODEL = "Dummy"

    # Device
    DEVICE = "cpu"  # Future: "cuda"

    # Model folders
    MODEL_DIRECTORY = Path("models")
    WEIGHTS_DIRECTORY = MODEL_DIRECTORY / "weights"

    # Detection parameters
    CONFIDENCE_THRESHOLD = 0.25
    IOU_THRESHOLD = 0.45

    # Image settings
    IMAGE_SIZE = 640

    # Performance
    HALF_PRECISION = False
    MAX_AI_FPS = 30

    # Overlay
    DRAW_LABELS = True
    DRAW_CONFIDENCE = True
    DRAW_BOXES = True