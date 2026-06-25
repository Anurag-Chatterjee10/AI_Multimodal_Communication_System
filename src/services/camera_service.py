"""
Camera Service
--------------
Manages the application's camera subsystem.
"""

import cv2

from PySide6.QtCore import (
    QObject,
    Signal,
)

from src.core.logger import logger
from src.services.camera_thread import CameraThread


class CameraService(QObject):
    """
    Camera Service.
    """

    camera_started = Signal()

    camera_stopped = Signal()

    frame_ready = Signal(object)

    fps_updated = Signal(float)

    camera_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Initializing Camera Service")

        self._current_camera = 0

        self._thread = None

    # ======================================================
    # Properties
    # ======================================================

    @property
    def is_running(self):
        """
        Returns whether the camera is running.
        """

        return (
            self._thread is not None
            and self._thread.is_running
        )

    @property
    def current_camera(self):
        """
        Returns the current camera index.
        """

        return self._current_camera

    # ======================================================
    # Camera Enumeration
    # ======================================================

    def enumerate_cameras(
        self,
        max_devices: int = 10,
    ) -> list[int]:
        """
        Detect available camera devices.
        """

        logger.info("Enumerating cameras...")

        cameras = []

        for index in range(max_devices):

            capture = cv2.VideoCapture(index)

            if capture.isOpened():

                success, _ = capture.read()

                if success:

                    cameras.append(index)

            capture.release()

        logger.info(
            f"Available cameras: {cameras}"
        )

        return cameras

    # ======================================================
    # Camera Control
    # ======================================================

    def start(
        self,
        camera_index: int | None = None,
    ):
        """
        Start camera.
        """

        if self.is_running:

            logger.warning(
                "Camera already running."
            )

            return

        if camera_index is not None:

            self._current_camera = camera_index

        logger.info(
            f"Starting Camera {self._current_camera}"
        )

        self._thread = CameraThread(
            self._current_camera
        )

        self._connect_signals()

        self._thread.start()

    def stop(self):
        """
        Stop camera.
        """

        if not self.is_running:

            return

        logger.info("Stopping Camera")
        thread = self._thread

        if thread is not None:
            thread.stop()

    def switch_camera(
        self,
        camera_index: int,
    ):
        """
        Switch to another camera.
        """

        if camera_index == self._current_camera:

            logger.info(
                "Camera already selected."
            )

            return

        logger.info(
            f"Switching camera "
            f"{self._current_camera} -> {camera_index}"
        )

        was_running = self.is_running

        if was_running:

            self.stop()

        self._current_camera = camera_index

        if was_running:

            self.start()

    # ======================================================
    # Signal Connections
    # ======================================================

    def _connect_signals(self):
        """
        Forward CameraThread signals.
        """

        if self._thread is None:

            return

        self._thread.camera_started.connect(
            self.camera_started.emit
        )

        self._thread.camera_stopped.connect(
            self._on_camera_stopped
        )

        self._thread.frame_ready.connect(
            self.frame_ready.emit
        )

        self._thread.fps_updated.connect(
            self.fps_updated.emit
        )

        self._thread.camera_error.connect(
            self.camera_error.emit
        )
    
    def _on_camera_stopped(self):
        """
        Called after the camera thread has completely stopped.
        """

        self.camera_stopped.emit()

        self._thread = None