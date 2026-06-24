"""
Base AI Model

Every AI model used by the application will inherit from this base class.

Examples:
- YOLO
- EasyOCR
- Whisper
- Face Recognition
"""
"""
Base AI Model

Every AI model in the application must inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    """
    Abstract base class for all AI models.
    """

    def __init__(
        self,
        model_name: str,
        version: str = "1.0",
        author: str = "Unknown",
        description: str = ""
    ):
        self._model_name = model_name
        self._version = version
        self._author = author
        self._description = description
        self._loaded = False

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def author(self) -> str:
        return self._author

    @property
    def description(self) -> str:
        return self._description

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def metadata(self) -> dict:
        """
        Returns all metadata in a dictionary.
        """
        return {
            "name": self._model_name,
            "version": self._version,
            "author": self._author,
            "description": self._description,
            "loaded": self._loaded,
        }

    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def unload(self) -> None:
        pass

    @abstractmethod
    def infer(self, data: Any) -> Any:
        pass