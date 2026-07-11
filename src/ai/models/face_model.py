"""
Face Recognition Model
"""

from typing import Any

from src.ai.face.face_engine import FaceEngine
from src.ai.models.base_model import BaseModel
from src.ai.results.face_result import FaceResult


class FaceModel(BaseModel):
    """
    Face Recognition AI Model.
    """

    def __init__(self):
        super().__init__(
            model_name="Face",
            version="1.0",
            author="InsightFace",
            description="Face Detection and Recognition",
        )

        self._engine = FaceEngine()

    def load(self) -> None:
        """
        Loads the Face Recognition engine.
        """

        if self._loaded:
            return

        self._engine.load()

        self._loaded = True

    def unload(self) -> None:
        """
        Unloads the Face Recognition engine.
        """

        if not self._loaded:
            return

        self._engine.unload()

        self._loaded = False

    def infer(
        self,
        data: Any,
    ) -> FaceResult:
        """
        Performs face recognition.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face model is not loaded."
            )

        recognized_faces = self._engine.recognize(data)

        result = FaceResult(
            model_name=self.model_name,
            success=True,
        )

        for face in recognized_faces:

            result.add_face(
                identity=face["identity"],
                confidence=face["confidence"],
                bbox=face["bbox"],
            )

        return result