"""
Audio Buffer
------------

Maintains a rolling buffer of microphone audio for
speech recognition.
"""

from collections import deque

import numpy as np


class AudioBuffer:
    """
    Rolling audio buffer.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        max_seconds: int = 5,
    ):
        self._sample_rate = sample_rate
        self._max_seconds = max_seconds

        self._buffer = deque()

        self._max_samples = (
            sample_rate * max_seconds
        )

        self._current_samples = 0

    @property
    def sample_rate(self) -> int:
        """
        Returns the configured sample rate.
        """
        return self._sample_rate

    @property
    def duration(self) -> float:
        """
        Returns the current buffered duration in seconds.
        """
        return self._current_samples / self._sample_rate

    def append(self, audio: np.ndarray) -> None:
        """
        Append new audio samples to the buffer.
        """

        if audio.size == 0:
            return

        self._buffer.append(audio)

        self._current_samples += len(audio)

        while (
            self._current_samples
            > self._max_samples
        ):
            old = self._buffer.popleft()

            self._current_samples -= len(old)

    def get_audio(self) -> np.ndarray:
        """
        Return all buffered audio as one NumPy array.
        """

        if not self._buffer:
            return np.array([], dtype=np.float32)

        return np.concatenate(
            list(self._buffer)
        ).astype(np.float32)

    def clear(self) -> None:
        """
        Remove all buffered audio.
        """

        self._buffer.clear()

        self._current_samples = 0

    def is_ready(
        self,
        minimum_seconds: float = 2.0,
    ) -> bool:
        """
        Returns True if enough audio is available.
        """

        return self.duration >= minimum_seconds