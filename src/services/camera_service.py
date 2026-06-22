"""
Camera Service
--------------
Manages the application's camera subsystem.
"""

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

        self._thread = CameraThread()

        self._connect_signals()

    @property
    def is_running(self):
        return self._thread.is_running

    def start(self):
        """
        Start camera.
        """

        if self._thread.is_running:
            return

        logger.info("Starting Camera")

        self._thread.start()

    def stop(self):
        """
        Stop camera.
        """

        if self._thread.is_running:

            logger.info("Stopping Camera")

            self._thread.stop()

    def _connect_signals(self):
        """
        Forward CameraThread signals.
        """

        self._thread.camera_started.connect(
            self.camera_started.emit
        )

        self._thread.camera_stopped.connect(
            self.camera_stopped.emit
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