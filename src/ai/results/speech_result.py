"""
Speech Result

Represents the output of a Speech-to-Text model.
"""

from .base_result import BaseResult


class SpeechResult(BaseResult):
    """
    Stores speech recognition results.
    """

    def __init__(
        self,
        model_name: str,
        success: bool,
        transcript: str = "",
        confidence: float = 0.0,
        language: str = "",
        duration: float = 0.0,
        message: str = "",
    ):
        self._transcript = transcript
        self._confidence = confidence
        self._language = language
        self._duration = duration

        super().__init__(
            model_name=model_name,
            success=success,
            data=transcript,
            message=message,
        )

    @property
    def transcript(self) -> str:
        """
        Returns the recognized speech.
        """
        return self._transcript

    @property
    def confidence(self) -> float:
        """
        Returns the recognition confidence.
        """
        return self._confidence

    @property
    def language(self) -> str:
        """
        Returns the detected language.
        """
        return self._language

    @property
    def duration(self) -> float:
        """
        Returns the speech duration in seconds.
        """
        return self._duration

    def to_dict(self) -> dict:
        """
        Converts the speech result into a dictionary.
        """

        result = super().to_dict()

        result["transcript"] = self.transcript
        result["confidence"] = self.confidence
        result["language"] = self.language
        result["duration"] = self.duration

        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model='{self.model_name}', "
            f"language='{self.language}', "
            f"success={self.success})"
        )