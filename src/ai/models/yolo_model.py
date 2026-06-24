"""
YOLO AI Model

Loads the Ultralytics YOLO model into the application.
"""

from pathlib import Path
from typing import Any

from ultralytics import YOLO

from src.ai.models.base_model import BaseModel
from src.ai.results.detection_result import DetectionResult


class YOLOModel(BaseModel):
    """
    YOLO object detection model.
    """

    def __init__(self):
        super().__init__(
            model_name="YOLO",
            version="8",
            author="Ultralytics",
            description="YOLO Object Detection Model"
        )

        self._model = None
        self._weights_path = Path("models") / "weights" / "yolov8n.pt"

    def load(self) -> None:
        """
        Load the YOLO model from disk.
        """

        if self._loaded:
            return

        if not self._weights_path.exists():
            raise FileNotFoundError(
                f"Weight file not found: {self._weights_path}"
            )

        self._model = YOLO(str(self._weights_path))

        self._loaded = True

    def unload(self) -> None:
        """
        Unload the YOLO model from memory.
        """

        if not self._loaded:
            return

        self._model = None

        self._loaded = False

    def infer(self, data: Any) -> DetectionResult:
        """
        Run YOLO inference.
        """

        if not self._loaded:
            raise RuntimeError("YOLO model is not loaded.")

        yolo_results = self._model.predict(
            source=data,
            verbose=False
        )

        return self._parse_results(yolo_results)
    def _parse_results(self, yolo_results) -> DetectionResult:
        """
        Convert Ultralytics results into DetectionResult.
        """

        result = DetectionResult(
            model_name=self.model_name,
            success=True,
            message="YOLO inference completed."
        )

        prediction = yolo_results[0]

        for box in prediction.boxes:

            class_id = int(box.cls.item())

            label = prediction.names[class_id]

            confidence = float(box.conf.item())

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            result.add_detection(
                label=label,
                confidence=confidence,
                bbox=[x1, y1, x2, y2]
            )

        return result