"""
Speech Model

Speech recognition model using Faster-Whisper.
"""

from typing import Any

import numpy as np
from faster_whisper import WhisperModel

from src.ai.models.base_model import BaseModel
from src.ai.results.speech_result import SpeechResult


class SpeechModel(BaseModel):
    """
    Speech recognition model.
    """

    def __init__(self):
        super().__init__(
            model_name="Speech",
            version="1.0",
            author="Faster-Whisper",
            description="Real-time speech recognition using Faster-Whisper",
        )

        self._model = None

    def load(self) -> None:
        """
        Load the Whisper model.
        """

        if self._loaded:
            return

        self._model = WhisperModel(
            model_size_or_path="base",
            device="cpu",
            compute_type="float32",
        )

        self._loaded = True
    def unload(self) -> None:
        """
        Release the model.
        """

        self._model = None
        self._loaded = False

    def infer(self, data: Any) -> SpeechResult:
        """
        Perform speech recognition.

        Parameters
        ----------
        data
            NumPy float32 audio sampled at 16 kHz.

        Returns
        -------
        SpeechResult
        """

        if not self._loaded:
            raise RuntimeError(
                "Speech model is not loaded."
            )

        if not isinstance(data, np.ndarray):
            raise TypeError(
                "SpeechModel expects a NumPy array."
            )

        try:

            segments, info = self._model.transcribe(
                data,
                beam_size=5,
            )

            transcript = " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

            return SpeechResult(
                model_name=self.model_name,
                success=True,
                transcript=transcript,
                confidence=1.0,
                language=info.language,
                duration=info.duration,
            )

        except Exception as e:

            return SpeechResult(
                model_name=self.model_name,
                success=False,
                message=str(e),
            )