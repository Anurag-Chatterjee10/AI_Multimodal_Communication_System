"""
Model Manager

This module will manage the complete lifecycle of AI models.

Future responsibilities:
- Load models
- Unload models
- Track loaded models
- Device selection
- Memory management
- Model metadata
"""
"""
Model Manager

Central manager responsible for controlling AI models.
"""

from typing import List, Optional
from src.ai.models.dummy_model import DummyModel
from src.ai.managers.model_registry import ModelRegistry
from src.ai.models.base_model import BaseModel


class ModelManager:
    """
    Central manager responsible for all AI models.
    """

    def __init__(self):
        self._registry = ModelRegistry()

        self._register_builtin_models()

        self._active_model: BaseModel | None = None
    
    def _register_builtin_models(self) -> None:
        """
        Register all built-in AI models.
        """

        self.register_model(
            DummyModel()
        )

    def register_model(self, model: BaseModel) -> None:
        """
        Register an AI model.
        """
        self._registry.register_model(model)

    def unregister_model(self, model_name: str) -> None:
        """
        Remove an AI model.
        """
        self._registry.unregister_model(model_name)

    def load_model(self, model_name: str) -> None:
            """
            Load a registered model.
            """
            model = self._registry.get_model(model_name)

            if model is None:
                raise ValueError(f"Model '{model_name}' not found.")

            if not model.is_loaded:
                model.load()

            self._active_model = model
    def unload_model(self, model_name: str) -> None:
            """
            Unload a registered model.
            """
            model = self._registry.get_model(model_name)

            if model is None:
                raise ValueError(f"Model '{model_name}' not found.")

            if model.is_loaded:
                model.unload()
            
            if self._active_model == model:
                self._active_model = None

    def get_model(self, model_name: str) -> Optional[BaseModel]:
        """
        Return a registered model.
        """
        return self._registry.get_model(model_name)

    def has_model(self, model_name: str) -> bool:
        """
        Check whether a model exists.
        """
        return self._registry.has_model(model_name)

    def list_models(self) -> List[str]:
        """
        Return all registered model names.
        """
        return self._registry.list_models()

    @property
    def model_count(self) -> int:
        """
        Number of registered models.
        """
        return self._registry.model_count

    def shutdown(self) -> None:
        """
        Unload every loaded model and clear the registry.
        """
        for name in self.list_models():

            model = self.get_model(name)

            if model is not None and model.is_loaded:
                model.unload()

        self._registry.clear()
    
    @property
    def active_model(self) -> Optional[BaseModel]:
        """
        Returns the currently active AI model.
        """

        return self._active_model

    @property
    def active_model_name(self) -> str:
        """
        Returns the active model name.
        """

        if self._active_model is None:
            return "Not Loaded"

        return self._active_model.model_name