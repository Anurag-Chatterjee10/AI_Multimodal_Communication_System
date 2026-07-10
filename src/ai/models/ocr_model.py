"""
OCR Model

EasyOCR implementation for the AI framework.
"""

from typing import Any

import easyocr

from src.ai.models.base_model import BaseModel
from src.ai.results.ocr_result import OCRResult
from src.config import settings

class OCRModel(BaseModel):
    """
    OCR model using EasyOCR.
    """

    def __init__(self):
        super().__init__(
            model_name="OCR",
            version="1.0",
            author="EasyOCR",
            description="Optical Character Recognition using EasyOCR",
        )

        self._reader = None

    def load(self) -> None:
        """
        Loads the EasyOCR model into memory.
        """

        if self._loaded:
            return

        self._reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

        self._loaded = True

    def unload(self) -> None:
        """
        Unloads the model.
        """

        self._reader = None
        self._loaded = False

    def infer(self, data: Any) -> OCRResult:
        """
        Performs OCR inference.

        Parameters
        ----------
        data
            OpenCV image (NumPy ndarray)

        Returns
        -------
        OCRResult
        """

        if not self._loaded:
            raise RuntimeError(
                "OCR model is not loaded."
            )

        result = OCRResult(
            model_name=self.model_name,
            success=True,
        )

        try:

            detections = self._reader.readtext(data)

            for bbox, text, confidence in detections:

                if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
                    continue

                result.add_text(
                    text=text,
                    confidence=float(confidence),
                    bbox=bbox,
                )

            return result

        except Exception as e:

            return OCRResult(
                model_name=self.model_name,
                success=False,
                message=str(e),
            )