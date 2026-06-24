"""
OCR Result

Represents the output of an OCR model.
"""

from typing import Any

from .base_result import BaseResult


class OCRResult(BaseResult):
    """
    Stores OCR results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        text_regions: list[dict[str, Any]] | None = None,
        message: str = "",
    ):
        if text_regions is None:
            text_regions = []

        self._text_regions = text_regions

        super().__init__(
            model_name=model_name,
            success=success,
            data=self._text_regions,
            message=message,
        )

    @property
    def text_regions(self) -> list[dict[str, Any]]:
        """
        Returns all detected text regions.
        """
        return self._text_regions

    @property
    def region_count(self) -> int:
        """
        Returns the number of detected text regions.
        """
        return len(self._text_regions)

    @property
    def full_text(self) -> str:
        """
        Returns all detected text as a single string.
        """
        return " ".join(
            region["text"] for region in self._text_regions
        )

    def add_text(
        self,
        text: str,
        confidence: float,
        bbox: list[int],
    ) -> None:
        """
        Adds a detected text region.
        """

        self._text_regions.append(
            {
                "text": text,
                "confidence": confidence,
                "bbox": bbox,
            }
        )

    def clear(self) -> None:
        """
        Removes all detected text.
        """
        self._text_regions.clear()

    def to_dict(self) -> dict:
        """
        Converts the OCR result into a dictionary.
        """

        result = super().to_dict()

        result["region_count"] = self.region_count
        result["full_text"] = self.full_text
        result["text_regions"] = self.text_regions

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"regions={self.region_count}, "
            f"success={self.success})"
        )