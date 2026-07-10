"""
Microphone Service
------------------
Manages the application's microphone subsystem.
"""

import sounddevice as sd

from PySide6.QtCore import (
    QObject,
    Signal,
)

from src.core.logger import logger
from src.services.microphone.microphone_thread import MicrophoneThread


class MicrophoneService(QObject):
    """
    Microphone Service.
    """

    microphone_started = Signal()

    microphone_stopped = Signal()

    audio_ready = Signal(object)

    microphone_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Initializing Microphone Service")

        self._current_microphone = None

        self._thread = None

    # ======================================================
    # Properties
    # ======================================================

    @property
    def is_running(self):
        """
        Returns whether the microphone is running.
        """

        return (
            self._thread is not None
            and self._thread.is_running
        )

    @property
    def current_microphone(self):
        """
        Returns the current microphone.
        """

        return self._current_microphone

    # ======================================================
    # Device Enumeration
    # ======================================================

    def enumerate_microphones(self):
        """
        Detect available microphone devices.
        """

        logger.info("Enumerating microphones...")

        microphones = []

        devices = sd.query_devices()

        for index, device in enumerate(devices):

            if device["max_input_channels"] > 0:

                microphones.append(
                    {
                        "index": index,
                        "name": device["name"],
                    }
                )

        logger.info(
            f"Available microphones: {len(microphones)}"
        )

        return microphones

    # ======================================================
    # Control
    # ======================================================

    def start(
        self,
        microphone_index=None,
    ):
        """
        Start microphone.
        """

        if self.is_running:

            logger.warning(
                "Microphone already running."
            )

            return

        if microphone_index is not None:

            self._current_microphone = microphone_index

        logger.info(
            f"Starting Microphone {self._current_microphone}"
        )

        self._thread = MicrophoneThread(
            self._current_microphone
        )

        self._connect_signals()

        self._thread.start()

    def stop(self):
        """
        Stop microphone.
        """

        if not self.is_running:

            return

        logger.info("Stopping Microphone")

        if self._thread is not None:

            self._thread.stop()

    def switch_microphone(
        self,
        microphone_index,
    ):
        """
        Switch microphone.
        """

        if microphone_index == self._current_microphone:

            logger.info(
                "Microphone already selected."
            )

            return

        was_running = self.is_running

        if was_running:

            self.stop()

        self._current_microphone = microphone_index

        if was_running:

            self.start()

    # ======================================================
    # Signals
    # ======================================================

    def _connect_signals(self):

        if self._thread is None:

            return

        self._thread.microphone_started.connect(
            self.microphone_started.emit
        )

        self._thread.microphone_stopped.connect(
            self._on_microphone_stopped
        )

        self._thread.audio_ready.connect(
            self.audio_ready.emit
        )

        self._thread.microphone_error.connect(
            self.microphone_error.emit
        )

    def _on_microphone_stopped(self):

        self.microphone_stopped.emit()

        self._thread = None