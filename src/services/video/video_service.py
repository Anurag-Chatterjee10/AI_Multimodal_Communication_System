"""
Video Service
-------------

Provides a high-level interface for
video playback.
"""

from PySide6.QtCore import QObject, Signal

from src.core.logger import logger
from src.services.video.video_thread import VideoThread


class VideoService(QObject):
    """
    High-level interface for video playback.
    """

    video_started = Signal()

    video_finished = Signal()

    frame_ready = Signal(object)

    fps_updated = Signal(float)

    video_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Initializing Video Service")

        self._thread = None

        self._video_path = None

    @property
    def is_running(self):
        """
        Returns whether a video is
        currently playing.
        """

        return (
            self._thread is not None
            and self._thread.is_running
        )

    def open(self, video_path: str):
        """
        Open a video file.
        """

        self._video_path = video_path

    def start(self):
        """
        Start video playback.
        """

        if self._video_path is None:

            self.video_error.emit(
                "No video selected."
            )

            return

        if self.is_running:

            logger.warning(
                "Video already running."
            )

            return

        self._thread = VideoThread(
            self._video_path
        )

        self._thread.video_started.connect(
            self.video_started.emit
        )

        self._thread.video_finished.connect(
            self.video_finished.emit
        )

        self._thread.frame_ready.connect(
            self.frame_ready.emit
        )

        self._thread.fps_updated.connect(
            self.fps_updated.emit
        )

        self._thread.video_error.connect(
            self.video_error.emit
        )

        self._thread.start()

    def stop(self):
        """
        Stop playback.
        """

        if self._thread is None:

            return

        self._thread.stop()

        self._thread = None

    def pause(self):
        """
        Pause playback.
        """

        if self._thread is not None:

            self._thread.pause()

    def resume(self):
        """
        Resume playback.
        """

        if self._thread is not None:

            self._thread.resume()