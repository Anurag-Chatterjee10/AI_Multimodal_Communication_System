"""
Face Result

Represents the output of a face detection or recognition model.
"""

from typing import Any

from .base_result import BaseResult


class FaceResult(BaseResult):
    """
    Stores face detection and recognition results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        faces: list[dict[str, Any]] | None = None,
        message: str = "",
    ):
        if faces is None:
            faces = []

        self._faces = faces

        super().__init__(
            model_name=model_name,
            success=success,
            data=self._faces,
            message=message,
        )

    @property
    def faces(self) -> list[dict[str, Any]]:
        """
        Returns all detected faces.
        """
        return self._faces

    @property
    def face_count(self) -> int:
        """
        Returns the number of detected faces.
        """
        return len(self._faces)

    def add_face(
        self,
        identity: str,
        confidence: float,
        bbox: list[int],
    ) -> None:
        """
        Adds a detected face.
        """

        self._faces.append(
            {
                "identity": identity,
                "confidence": confidence,
                "bbox": bbox,
            }
        )

    def clear(self) -> None:
        """
        Removes all detected faces.
        """

        self._faces.clear()

    def to_dict(self) -> dict:
        """
        Converts the face result into a dictionary.
        """

        result = super().to_dict()

        result["face_count"] = self.face_count
        result["faces"] = self.faces

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"faces={self.face_count}, "
            f"success={self.success})"
        )