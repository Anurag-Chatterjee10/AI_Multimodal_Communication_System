"""
Segmentation Result

Represents the output of an image segmentation model.
"""

from typing import Any

from .base_result import BaseResult


class SegmentationResult(BaseResult):
    """
    Stores image segmentation results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        segments: list[dict[str, Any]] | None = None,
        message: str = "",
    ):
        if segments is None:
            segments = []

        self._segments = segments

        super().__init__(
            model_name=model_name,
            success=success,
            data=self._segments,
            message=message,
        )

    @property
    def segments(self) -> list[dict[str, Any]]:
        """
        Returns all segmented objects.
        """
        return self._segments

    @property
    def segment_count(self) -> int:
        """
        Returns the number of segmented objects.
        """
        return len(self._segments)

    def add_segment(
        self,
        label: str,
        confidence: float,
        mask: Any,
    ) -> None:
        """
        Adds a segmented object.
        """

        self._segments.append(
            {
                "label": label,
                "confidence": confidence,
                "mask": mask,
            }
        )

    def clear(self) -> None:
        """
        Removes all segmentation results.
        """

        self._segments.clear()

    def to_dict(self) -> dict:
        """
        Converts the segmentation result into a dictionary.
        """

        result = super().to_dict()

        result["segment_count"] = self.segment_count
        result["segments"] = self.segments

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"segments={self.segment_count}, "
            f"success={self.success})"
        )