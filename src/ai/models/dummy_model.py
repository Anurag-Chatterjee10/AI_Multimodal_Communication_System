"""
Dummy AI Model

Temporary AI model used to validate the
AI infrastructure before integrating
real AI models.
"""

from typing import Any
from src.ai.results.detection_result import DetectionResult
from src.ai.models.base_model import BaseModel


class DummyModel(BaseModel):
    """
    Simple placeholder AI model.
    """

    def __init__(self):
        super().__init__(
            model_name="Dummy",
            version="1.0",
            author="AI Multimodal Communication System",
            description="Application placeholder model"
        )

    def load(self) -> None:
        """
        Simulate model loading.
        """
        self._loaded = True

    def unload(self) -> None:
        """
        Simulate model unloading.
        """
        self._loaded = False

    def infer(self, data: Any) -> DetectionResult:
        """
        Perform placeholder inference.
        """

        from src.ai.results.detection_result import DetectionResult

        result = DetectionResult(
            model_name=self.model_name,
            success=True,
            message="Dummy inference completed."
        )

        result.add_detection(
            label="Dummy Object",
            confidence=1.0,
            bbox=[100, 100, 300, 300],
        )

        return result