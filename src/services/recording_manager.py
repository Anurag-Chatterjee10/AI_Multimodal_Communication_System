"""
Recording Manager

Handles video recording using OpenCV VideoWriter.
This class manages the recording lifecycle without
interfering with camera capture or frame processing.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional

import cv2
import numpy as np

from src.core.logger import logger


class RecordingManager:
    """
    Manages video recording using OpenCV VideoWriter.

    This class is responsible only for recording video.
    It does not interact with the camera, UI, or frame
    acquisition. Frames are supplied externally by the
    FramePipeline.
    """

    def __init__(self, output_directory: str = "exports/videos") -> None:
        """
        Initialize the recording manager.

        Args:
            output_directory:
                Directory where recorded videos will be saved.
        """

        self._output_directory = Path(output_directory)
        self._output_directory.mkdir(parents=True, exist_ok=True)

        self._writer: Optional[cv2.VideoWriter] = None
        self._recording: bool = False

        self._output_path: Optional[Path] = None
        self._start_time: Optional[datetime] = None

        logger.info("RecordingManager initialized.")

    @property
    def is_recording(self) -> bool:
        """
        Returns whether recording is currently active.
        """
        return self._recording

    @property
    def output_path(self) -> Optional[Path]:
        """
        Returns the current output video path.
        """
        return self._output_path

    @property
    def start_time(self) -> Optional[datetime]:
        """
        Returns the recording start time.
        """
        return self._start_time

    def start_recording(
        self,
        filename: Optional[str],
        fps: float,
        frame_size: tuple[int, int],
    ) -> bool:
        """
        Starts a new video recording.

        Args:
            filename:
                Name of the output video file.
                If None, a timestamp-based filename is generated.

            fps:
                Recording frame rate.

            frame_size:
                Frame size as (width, height).

        Returns:
            True if recording started successfully,
            otherwise False.
        """

        if self._recording:
            logger.warning("Recording already in progress.")
            return False

        try:
            if filename is None:
                filename = datetime.now().strftime(
                    "recording_%Y%m%d_%H%M%S.mp4"
                )

            self._output_path = self._output_directory / filename

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            self._writer = cv2.VideoWriter(
                str(self._output_path),
                fourcc,
                fps,
                frame_size,
            )

            if not self._writer.isOpened():
                logger.error("Failed to create VideoWriter.")
                self._writer = None
                return False

            self._recording = True
            self._start_time = datetime.now()

            logger.info(
                f"Recording started: {self._output_path}"
            )

            return True

        except Exception as error:
            logger.exception(
                f"Failed to start recording: {error}"
            )

            self._writer = None
            self._recording = False
            self._output_path = None
            self._start_time = None

            return False

    def write_frame(self, frame: np.ndarray) -> None:
        """
        Writes a single frame to the recording.

        Args:
            frame:
                OpenCV image frame.
        """

        if (
            self._recording
            and self._writer is not None
            and frame is not None
        ):
            self._writer.write(frame)

    def stop_recording(self) -> None:
        """
        Stops the current recording and releases resources.
        """

        if not self._recording:
            logger.warning("No active recording to stop.")
            return

        if self._writer is not None:
            self._writer.release()

        logger.info("Recording stopped.")

        self._writer = None
        self._recording = False
        self._output_path = None
        self._start_time = None