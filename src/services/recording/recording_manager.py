"""
Recording Manager
-----------------
Handles video recording using OpenCV VideoWriter.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

import cv2


class RecordingManager:
    """
    Handles video recording.
    """

    def __init__(self, output_directory: str = "exports/videos") -> None:
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

        self._writer = None
        self._is_recording = False
        self._output_path = None

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    @property
    def output_path(self):
        return self._output_path

    def start_recording(
        self,
        frame_width: int,
        frame_height: int,
        fps: float,
    ) -> bool:

        if self._is_recording:
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self._output_path = (
            self.output_directory /
            f"recording_{timestamp}.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self._writer = cv2.VideoWriter(
            str(self._output_path),
            fourcc,
            fps,
            (frame_width, frame_height),
        )

        if not self._writer.isOpened():
            self._writer = None
            return False

        self._is_recording = True
        return True

    def write_frame(self, frame) -> None:

        if not self._is_recording:
            return

        if self._writer is None:
            return

        self._writer.write(frame)

    def stop_recording(self) -> None:

        if self._writer is not None:
            self._writer.release()

        self._writer = None
        self._is_recording = False

    def shutdown(self) -> None:
        self.stop_recording()