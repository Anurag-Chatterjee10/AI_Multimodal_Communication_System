"""
Detection Result

Represents the output of an object detection model.
"""

from typing import Any

from .base_result import BaseResult


class DetectionResult(BaseResult):
    """
    Stores object detection results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        detections: list[dict[str, Any]] | None = None,
        message: str = "",
    ):
        if detections is None:
            detections = []

        self._detections = detections

        super().__init__(
            model_name=model_name,
            success=success,
            data=self._detections,
            message=message,
        )

    @property
    def detections(self) -> list[dict[str, Any]]:
        """
        Returns all detections.
        """
        return self._detections

    @property
    def object_count(self) -> int:
        """
        Returns the number of detected objects.
        """
        return len(self._detections)

    def add_detection(
        self,
        label: str,
        confidence: float,
        bbox: list[int],
    ) -> None:
        """
        Adds a new detected object.
        """

        self._detections.append(
            {
                "label": label,
                "confidence": confidence,
                "bbox": bbox,
            }
        )

    def clear(self) -> None:
        """
        Removes all detections.
        """

        self._detections.clear()

    def to_dict(self) -> dict:
        """
        Converts the result into a dictionary.
        """

        result = super().to_dict()

        result["object_count"] = self.object_count
        result["detections"] = self.detections

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"objects={self.object_count}, "
            f"success={self.success})"
        )