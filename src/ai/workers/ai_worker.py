"""
AI Worker

This module will contain the background inference thread.

The worker will receive frames from the Frame Pipeline,
perform AI inference,
and return structured results without blocking the UI.
"""
"""
AI Worker

Architecture definition for the background AI inference worker.

Responsibilities
----------------
- Receive frames from the Frame Pipeline.
- Perform AI inference in a background thread.
- Emit structured AI results.
- Never block the GUI.
- Support future AI models through the ModelManager.

Future Workflow
---------------

Frame Pipeline
        │
        ▼
 AI Worker (QThread)
        │
        ▼
 Model Manager
        │
        ▼
 AI Model
        │
        ▼
 AI Result
        │
        ▼
 Overlay Engine
        │
        ▼
 Display
"""
"""
AI Worker

Background thread responsible for AI inference.
"""

from typing import Any

from PySide6.QtCore import QThread, Signal

from src.ai.managers.model_manager import ModelManager


class AIWorker(QThread):
    """
    Background worker responsible for AI inference.
    """

    inference_started = Signal()
    inference_finished = Signal(object)
    inference_error = Signal(str)

    def __init__(self, model_manager: ModelManager):
        super().__init__()

        self._model_manager = model_manager

        self._input_data = None

        self._model_name = None

        self._running = False

        self._busy = False
    
    def set_input(self, data: Any) -> bool:
        """
        Supply generic input for inference.

        Returns True if accepted.
        Returns False if the worker is busy.
        """

        if self._busy:
            return False

        self._input_data = data

        return True

    @property
    def is_busy(self) -> bool:
        """
        Returns whether the worker is currently processing a frame.
        """
        return self._busy

    def set_frame(self, frame: Any) -> bool:
        """
        Backward-compatible wrapper for vision models.
        """

        return self.set_input(frame)
    
    def set_model(self, model_name: str) -> None:
        """
        Select the AI model.
        """

        self._model_name = model_name

    def stop(self) -> None:
        """
        Stop the worker.
        """

        self._running = False

    def run(self) -> None:

        self._running = True

        self._busy = True

        self.inference_started.emit()

        try:

            result = self._process_input()

            self.inference_finished.emit(result)

        except Exception as error:

            self.inference_error.emit(str(error))

        finally:

            self._busy = False

            self._running = False

    def _process_input(self):

        if self._input_data is None:
            raise ValueError("No inference input supplied.")

        if self._model_name is None:
            raise ValueError("No AI model selected.")

        model = self._model_manager.get_model(self._model_name)

        if model is None:
            raise ValueError(
                f"Model '{self._model_name}' not found."
            )

        if not model.is_loaded:
            raise RuntimeError(
                f"Model '{self._model_name}' is not loaded."
            )

        return model.infer(self._input_data)