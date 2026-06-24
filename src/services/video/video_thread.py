"""
Video Thread
------------
Runs video playback in a background thread.
"""

import time

import cv2

from PySide6.QtCore import (
    QThread,
    Signal,
)

from src.core.logger import logger


class VideoThread(QThread):
    """
    Background thread responsible for
    video playback.
    """

    video_started = Signal()

    video_finished = Signal()

    frame_ready = Signal(object)

    fps_updated = Signal(float)

    video_error = Signal(str)

    def __init__(
        self,
        video_path: str,
        parent=None,
    ):
        super().__init__(parent)

        logger.info("Initializing Video Thread")

        self._video_path = video_path

        self._running = False

        self._paused = False

        self._capture = None

    @property
    def is_running(self):
        """
        Returns whether the thread
        is currently running.
        """

        return self._running

    def run(self):
        """
        Thread entry point.
        """

        logger.info(
            f"Opening Video : {self._video_path}"
        )

        self._capture = cv2.VideoCapture(
            self._video_path
        )

        if not self._capture.isOpened():

            logger.error(
                "Unable to open video."
            )

            self.video_error.emit(
                "Unable to open video."
            )

            return

        fps = self._capture.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:

            fps = 30.0

        frame_delay = 1.0 / fps

        self._running = True

        self.video_started.emit()

        while self._running:

            if self._paused:

                self.msleep(10)

                continue

            success, frame = self._capture.read()

            if not success:

                break

            self.frame_ready.emit(frame)

            self.fps_updated.emit(fps)

            time.sleep(frame_delay)

        if self._capture is not None:

            self._capture.release()

            self._capture = None

        self._running = False

        self.video_finished.emit()

        logger.info(
            "Video Thread Finished"
        )

    def pause(self):
        """
        Pause playback.
        """

        logger.info("Video Paused")

        self._paused = True

    def resume(self):
        """
        Resume playback.
        """

        logger.info("Video Resumed")

        self._paused = False

    def stop(self):
        """
        Gracefully stop playback.
        """

        if not self._running:

            return

        logger.info(
            "Stopping Video Thread"
        )

        self._running = False

        self.wait()