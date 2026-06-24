"""
Pose Result

Represents the output of a human pose estimation model.
"""

from typing import Any

from .base_result import BaseResult


class PoseResult(BaseResult):
    """
    Stores pose estimation results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        poses: list[dict[str, Any]] | None = None,
        message: str = "",
    ):
        if poses is None:
            poses = []

        self._poses = poses

        super().__init__(
            model_name=model_name,
            success=success,
            data=self._poses,
            message=message,
        )

    @property
    def poses(self) -> list[dict[str, Any]]:
        """
        Returns all detected poses.
        """
        return self._poses

    @property
    def person_count(self) -> int:
        """
        Returns the number of detected persons.
        """
        return len(self._poses)

    def add_pose(
        self,
        keypoints: list[dict[str, float]],
        confidence: float,
    ) -> None:
        """
        Adds a detected pose.
        """

        self._poses.append(
            {
                "keypoints": keypoints,
                "confidence": confidence,
            }
        )

    def clear(self) -> None:
        """
        Removes all stored poses.
        """

        self._poses.clear()

    def to_dict(self) -> dict:
        """
        Converts the pose result into a dictionary.
        """

        result = super().to_dict()

        result["person_count"] = self.person_count
        result["poses"] = self.poses

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"persons={self.person_count}, "
            f"success={self.success})"
        )