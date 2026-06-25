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

    def __init__(
        self,
        camera_index: int = 0,
        parent=None,
    ):
        super().__init__(parent)

        logger.info("Initializing Camera Thread")

        self._running = False

        self._camera = None

        self._camera_index = camera_index

    @property
    def is_running(self):
        """
        Returns whether the thread is running.
        """

        return self._running

    @property
    def camera_index(self):
        """
        Returns the current camera index.
        """

        return self._camera_index

    def set_camera(self, camera_index: int):
        """
        Set the camera index.

        This method should only be called
        while the thread is not running.
        """

        if self._running:

            logger.warning(
                "Cannot change camera while running."
            )

            return

        self._camera_index = camera_index

        logger.info(
            f"Camera index set to {camera_index}"
        )

    def run(self):
        """
        Thread entry point.
        """

        logger.info(
            f"Opening Camera {self._camera_index}"
        )

        self._camera = cv2.VideoCapture(
            self._camera_index
        )

        if not self._camera.isOpened():

            logger.error(
                f"Unable to open camera "
                f"{self._camera_index}"
            )

            self.camera_error.emit(
                f"Unable to open camera "
                f"{self._camera_index}."
            )

            return

        logger.info(
            f"Camera {self._camera_index} Opened"
        )

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

            fps = 1 / max(
                current_time - previous_time,
                0.000001,
            )

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