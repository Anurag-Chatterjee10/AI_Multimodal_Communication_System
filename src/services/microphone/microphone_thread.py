"""
Microphone Thread
-----------------
Runs microphone capture in a background thread.
"""

import numpy as np
import sounddevice as sd

from PySide6.QtCore import (
    QThread,
    Signal,
)

from src.core.logger import logger


class MicrophoneThread(QThread):
    """
    Background thread responsible for microphone capture.
    """

    microphone_started = Signal()

    microphone_stopped = Signal()

    audio_ready = Signal(object)

    microphone_error = Signal(str)

    def __init__(
        self,
        microphone_index=None,
        samplerate=16000,
        channels=1,
        chunk_size=16000,
        parent=None,
    ):
        super().__init__(parent)

        logger.info("Initializing Microphone Thread")

        self._running = False

        self._microphone_index = microphone_index

        self._samplerate = samplerate

        self._channels = channels

        self._chunk_size = chunk_size

    # ======================================================
    # Properties
    # ======================================================

    @property
    def is_running(self):
        """
        Returns whether the thread is running.
        """
        return self._running

    @property
    def microphone_index(self):
        """
        Returns the selected microphone index.
        """
        return self._microphone_index

    # ======================================================
    # Thread
    # ======================================================

    def run(self):
        """
        Thread entry point.
        """

        logger.info(
            f"Opening Microphone {self._microphone_index}"
        )

        self._running = True

        self.microphone_started.emit()

        try:

            with sd.InputStream(
                samplerate=self._samplerate,
                channels=self._channels,
                dtype="float32",
                blocksize=self._chunk_size,
                device=self._microphone_index,
            ) as stream:

                while self._running:

                    audio, overflow = stream.read(
                        self._chunk_size
                    )

                    if overflow:

                        logger.warning(
                            "Microphone buffer overflow."
                        )

                    audio = np.squeeze(audio)

                    self.audio_ready.emit(audio)

        except Exception as error:

            logger.exception(
                "Microphone thread failed."
            )

            self.microphone_error.emit(
                str(error)
            )

        finally:

            self._running = False

            self.microphone_stopped.emit()

            logger.info(
                "Microphone Thread Finished"
            )

    # ======================================================
    # Control
    # ======================================================

    def stop(self):
        """
        Gracefully stop the microphone thread.
        """

        if not self._running:
            return

        logger.info(
            "Stopping Microphone Thread"
        )

        self._running = False

        self.wait()