"""
Model Registry

Maintains a registry of AI models used by the application.
"""

from typing import Dict, List, Optional

from src.ai.models.base_model import BaseModel


class ModelRegistry:
    """
    Stores and manages AI model instances.
    """

    def __init__(self):
        self._models: Dict[str, BaseModel] = {}

    def register_model(self, model: BaseModel) -> None:
        """
        Register a model.

        Raises:
            ValueError: If a model with the same name already exists.
        """
        if model.model_name in self._models:
            raise ValueError(
                f"Model '{model.model_name}' is already registered."
            )

        self._models[model.model_name] = model

    def unregister_model(self, model_name: str) -> None:
        """
        Remove a model from the registry.
        """
        self._models.pop(model_name, None)

    def get_model(self, model_name: str) -> Optional[BaseModel]:
        """
        Return a registered model.
        """
        return self._models.get(model_name)

    def has_model(self, model_name: str) -> bool:
        """
        Check whether a model is registered.
        """
        return model_name in self._models

    def list_models(self) -> List[str]:
        """
        Return all registered model names.
        """
        return list(self._models.keys())

    def clear(self) -> None:
        """
        Remove every registered model.
        """
        self._models.clear()

    @property
    def model_count(self) -> int:
        """
        Return the number of registered models.
        """
        return len(self._models)