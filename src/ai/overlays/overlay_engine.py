"""
Overlay Engine

Responsible for rendering AI results on image frames.
"""

from __future__ import annotations

import cv2
import numpy as np

from src.ai.results.base_result import BaseResult
from src.ai.results.detection_result import DetectionResult
from src.ai.results.ocr_result import OCRResult
from src.ai.results.face_result import FaceResult
from src.ai.results.pose_result import PoseResult
from src.ai.results.segmentation_result import SegmentationResult


class OverlayEngine:
    """
    Central overlay manager.
    """

    def __init__(self):
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def toggle(self) -> None:
        self._enabled = not self._enabled

    def render(
        self,
        frame: np.ndarray,
        result: BaseResult | None,
    ) -> np.ndarray:

        if not self.enabled:
            return frame

        if result is None:
            return frame

        if isinstance(result, DetectionResult):
            self._draw_detection(frame, result)

        elif isinstance(result, OCRResult):
            self._draw_ocr(frame, result)

        elif isinstance(result, FaceResult):
            self._draw_face(frame, result)

        elif isinstance(result, PoseResult):
            self._draw_pose(frame, result)

        elif isinstance(result, SegmentationResult):
            self._draw_segmentation(frame, result)

        return frame

    def _draw_detection(self, frame, result):

        for detection in result.detections:

            label = detection["label"]
            confidence = detection["confidence"]
            x1, y1, x2, y2 = detection["bbox"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"{label} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

    def _draw_ocr(self, frame, result):

        for region in result.text_regions:

            text = region["text"]
            confidence = region["confidence"]
            x1, y1, x2, y2 = region["bbox"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            cv2.putText(
                frame,
                f"{text} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

    def _draw_face(self, frame, result):

        for face in result.faces:

            identity = face["identity"]
            confidence = face["confidence"]
            x1, y1, x2, y2 = face["bbox"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

            cv2.putText(
                frame,
                f"{identity} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

    def _draw_pose(self, frame, result):

        for pose in result.poses:

            for point in pose["keypoints"]:

                x = int(point["x"])
                y = int(point["y"])

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (255, 0, 255),
                    -1,
                )

    def _draw_segmentation(
        self,
        frame: np.ndarray,
        result: SegmentationResult,
    ) -> None:
        """
        Draw segmentation masks.

        Placeholder implementation.
        Actual mask rendering will be implemented
        when a real segmentation model is integrated.
        """

        for segment in result.segments:

            label = segment["label"]
            confidence = segment["confidence"]

            cv2.putText(
                frame,
                f"{label} {confidence:.2f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

    def clear(
        self,
        frame: np.ndarray,
    ) -> np.ndarray:
        return frame

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"enabled={self.enabled})"
        )