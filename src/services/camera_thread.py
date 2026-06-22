"""
Camera Thread
-------------
Runs camera operations in a background thread.
"""

import time

import cv2

from PySide6.QtCore import (
    QThread,
    Signal,
)

from src.core.logger import logger


class CameraThread(QThread):
    """
    Background thread responsible for camera operations.
    """

    camera_started = Signal()

    camera_stopped = Signal()

    frame_ready = Signal(object)

    fps_updated = Signal(float)

    camera_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Initializing Camera Thread")

        self._running = False

        self._camera = None

    @property
    def is_running(self):
        return self._running

    def run(self):
        """
        Thread entry point.
        """

        logger.info("Opening Camera")

        self._camera = cv2.VideoCapture(0)

        if not self._camera.isOpened():

            logger.error("Unable to open camera")

            self.camera_error.emit(
                "Unable to open camera."
            )

            return

        logger.info("Camera Opened")

        self._running = True

        self.camera_started.emit()

        previous_time = time.time()

        while self._running:

            success, frame = self._camera.read()

            if not success:

                self.camera_error.emit(
                    "Failed to read frame."
                )

                break

            self.frame_ready.emit(frame)

            current_time = time.time()

            fps = 1 / (current_time - previous_time)

            previous_time = current_time

            self.fps_updated.emit(fps)

            self.msleep(1)

        if self._camera is not None:

            self._camera.release()

            self._camera = None

        self._running = False

        self.camera_stopped.emit()

        logger.info("Camera Released")

        logger.info("Camera Thread Finished")

    def stop(self):
        """
        Gracefully stop the camera thread.
        """

        if not self._running:
            return

        logger.info("Stopping Camera Thread")

        self._running = False

        self.wait()