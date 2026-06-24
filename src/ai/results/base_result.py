"""
Base Result Object

Every AI result object will inherit from this class.

Examples:

- DetectionResult
- OCRResult
- FaceResult
- SpeechResult
"""
"""
Base AI Result

Defines the common structure shared by all AI result objects.
"""

from abc import ABC
from datetime import datetime
from typing import Any


class BaseResult(ABC):
    """
    Base class for every AI result.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        data: Any = None,
        message: str = "",
    ):
        self._model_name = model_name
        self._success = success
        self._data = data
        self._message = message
        self._timestamp = datetime.now()

    @property
    def model_name(self) -> str:
        """
        Returns the name of the AI model that produced this result.
        """
        return self._model_name

    @property
    def success(self) -> bool:
        """
        Returns whether inference was successful.
        """
        return self._success

    @property
    def data(self) -> Any:
        """
        Returns the model-specific result data.
        """
        return self._data

    @property
    def message(self) -> str:
        """
        Returns an informational message about the inference.
        """
        return self._message

    @property
    def timestamp(self) -> datetime:
        """
        Returns the time when this result object was created.
        """
        return self._timestamp

    def to_dict(self) -> dict:
        """
        Converts the result into a dictionary.
        Useful for logging, JSON export and debugging.
        """
        return {
            "model": self.model_name,
            "success": self.success,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"success={self.success})"
        )