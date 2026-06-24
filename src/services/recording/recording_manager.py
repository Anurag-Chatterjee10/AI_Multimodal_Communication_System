"""
Recording Manager
-----------------

Handles video recording for the application.

Responsibilities
----------------
• Start recording
• Stop recording
• Receive camera frames
• Save MP4 videos
"""

from pathlib import Path
from datetime import datetime
from typing import Optional

import cv2
import numpy as np

from PySide6.QtCore import QObject, Signal

from src.core.logger import logger


class RecordingManager(QObject):
    """
    Handles application video recording.

    This class records frames received from the
    FramePipeline and saves them as MP4 videos.
    """

    recording_started = Signal()
    recording_stopped = Signal()

    def __init__(
        self,
        output_directory: str = "exports/videos",
    ) -> None:
        """
        Initialize the Recording Manager.

        Args:
            output_directory:
                Directory where recordings are stored.
        """

        super().__init__()

        logger.info("Initializing Recording Manager")

        self._writer: Optional[cv2.VideoWriter] = None

        self._recording: bool = False

        self._output_path: Optional[Path] = None

        self._start_time: Optional[datetime] = None

        self._fps: float = 30.0

        self._output_directory = Path(output_directory)

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def is_recording(self) -> bool:
        """
        Returns recording status.
        """

        return self._recording

    @property
    def output_path(self) -> Optional[Path]:
        """
        Returns current output path.
        """

        return self._output_path

    @property
    def start_time(self) -> Optional[datetime]:
        """
        Returns recording start time.
        """

        return self._start_time

    # ======================================================
    # Recording
    # ======================================================

    def start(
        self,
        frame: np.ndarray,
        fps: float = 30.0,
    ) -> bool:
        """
        Start recording.
        """

        if self._recording:

            logger.warning(
                "Recording already in progress."
            )

            return False

        try:

            height, width = frame.shape[:2]

            self._fps = fps

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            self._output_path = (
                self._output_directory
                / f"recording_{timestamp}.mp4"
            )

            fourcc = cv2.VideoWriter_fourcc(
                *"mp4v"
            )

            self._writer = cv2.VideoWriter(
                str(self._output_path),
                fourcc,
                self._fps,
                (width, height),
            )

            if not self._writer.isOpened():

                logger.error(
                    "Unable to create VideoWriter."
                )

                self._writer = None

                return False

            self._recording = True

            self._start_time = datetime.now()

            logger.info(
                f"Recording started: "
                f"{self._output_path.name}"
            )

            self.recording_started.emit()

            return True

        except Exception as error:

            logger.exception(
                f"Recording start failed: {error}"
            )

            self._writer = None
            self._recording = False
            self._output_path = None
            self._start_time = None

            return False

    def write(
        self,
        frame: np.ndarray,
    ) -> None:
        """
        Write one frame to the video.
        """

        if (
            not self._recording
            or self._writer is None
            or frame is None
        ):
            return

        self._writer.write(frame)

    def stop(self) -> None:
        """
        Stop recording.
        """

        if not self._recording:

            logger.warning(
                "No active recording to stop."
            )

            return

        logger.info(
            "Stopping Recording"
        )

        if self._writer is not None:

            self._writer.release()

        self._writer = None

        self._recording = False

        self._output_path = None

        self._start_time = None

        self.recording_stopped.emit()

    def shutdown(self) -> None:
        """
        Shutdown the Recording Manager.
        """

        logger.info(
            "Shutting down Recording Manager"
        )

        self.stop()