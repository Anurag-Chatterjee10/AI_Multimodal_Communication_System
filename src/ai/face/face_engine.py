"""
Face Engine

Central backend for the Face Recognition system.

Responsibilities
----------------
- Load face recognition backend
- Build embedding database
- Detect faces
- Generate face embeddings
- Compare embeddings
- Return recognition results

Actual AI implementation will be added in later milestones.
"""

from pathlib import Path
from typing import Any
import src.config.settings as settings
import pickle
from src.core.logger import logger
import numpy as np
from src.ai.face.dataset_manager import FaceDatasetManager


class FaceEngine:
    """
    Core backend for Face Recognition.
    """

    def __init__(
        self,
        dataset_path: str = "datasets/faces",
    ):

        self._dataset = FaceDatasetManager(dataset_path)

        self._loaded = False

        self._detector = None

        self._recognizer = None

        self._embeddings: dict[str, list[Any]] = {}

        self._recognition_threshold = (
            settings.FACE_RECOGNITION_THRESHOLD
        )

        # Runtime statistics
        self._faces_processed = 0
        self._known_faces = 0
        self._unknown_faces = 0

        self._cache_file = (
            Path(dataset_path) / "embeddings.pkl"
        )

    @property
    def is_loaded(self) -> bool:
        """
        Returns whether the engine has been initialized.
        """
        return self._loaded

    @property
    def dataset(self) -> FaceDatasetManager:
        """
        Returns the dataset manager.
        """
        return self._dataset

    @property
    def embeddings(self) -> dict[str, list[Any]]:
        """
        Returns all stored embeddings.
        """
        return self._embeddings

    def load(self) -> None:
        """
        Initializes the Face Engine.
        """

        if self._loaded:
            return

        from insightface.app import FaceAnalysis
        import onnxruntime as ort

        # Load dataset metadata.
        self._dataset.load()

        available_providers = ort.get_available_providers()

        if "CUDAExecutionProvider" in available_providers:
            providers = [
                "CUDAExecutionProvider",
                "CPUExecutionProvider",
            ]
            ctx_id = 0
        else:
            providers = [
                "CPUExecutionProvider",
            ]
            ctx_id = -1

        self._detector = FaceAnalysis(
            name="buffalo_l",
            providers=providers,
        )

        self._detector.prepare(
            ctx_id=ctx_id,
            det_size=(640, 640),
        )

        self._recognizer = self._detector

        # Engine is now initialized.
        self._loaded = True

        logger.info("Face Engine initialized successfully.")

        # Load cached embeddings if available.
        if self.cache_exists:

            self._load_cache()

        else:

            self.build_database()

            logger.info(
                f"Face database loaded with "
                f"{self.dataset.identity_count} identities "
                f"and {self.dataset.image_count} images."
            )

            self._save_cache()

    def unload(self) -> None:
        """
        Releases resources.
        """

        self._detector = None

        self._recognizer = None

        self._embeddings.clear()

        self._loaded = False

        logger.info("Face Engine unloaded.")    

    def build_database(self) -> None:
        """
        Builds the embedding database from the dataset.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face Engine is not loaded."
            )

        self._embeddings.clear()

        for identity in self._dataset.identity_names:

            embeddings = []

            for image_path in self._dataset.get_images(identity):

                import cv2

                image = cv2.imread(str(image_path))

                if image is None:
                    continue

                faces = self.detect_faces(image)

                if not faces:
                    continue

                embedding = faces[0].embedding

                embedding = embedding / np.linalg.norm(
                    embedding
                )

                embeddings.append(embedding)

            if embeddings:
                self._embeddings[identity] = embeddings

    def _save_cache(self) -> None:
        """
        Saves embeddings to disk.
        """

        if not self._embeddings:
            return

        with open(
            self._cache_file,
            "wb",
        ) as file:

            pickle.dump(
                self._embeddings,
                file,
            )

    def _load_cache(self) -> None:
        """
        Loads embeddings from disk.
        """

        if not self.cache_exists:
            return

        with open(
            self._cache_file,
            "rb",
        ) as file:

            self._embeddings = pickle.load(file)

        expected = set(self._dataset.identity_names)
        cached = set(self._embeddings.keys())

        if expected != cached:

            self.build_database()

            self._save_cache()

    def detect_faces(
        self,
        image: Any,
    ) -> list:
        """
        Detects all faces in an image.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face Engine is not loaded."
            )

        faces = self._detector.get(image)

        return faces

    def generate_embedding(
        self,
        face: Any,
    ) -> Any:
        """
        Returns the embedding of a detected face.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face Engine is not loaded."
            )

        return face.embedding

    def compare_embedding(
        self,
        embedding: Any,
    ) -> tuple[str | None, float]:
        """
        Compare an embedding with the database.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face Engine is not loaded."
            )

        import numpy as np

        best_identity = None
        best_similarity = -1.0

        embedding = embedding / np.linalg.norm(embedding)

        for identity, embeddings in self._embeddings.items():

            for known in embeddings:

                known = known / np.linalg.norm(known)

                similarity = float(
                    np.dot(
                        embedding,
                        known,
                    )
                )

                if similarity > best_similarity:

                    best_similarity = similarity
                    best_identity = identity

        best_similarity = max(
            0.0,
            min(best_similarity, 1.0),
        )

        if best_similarity < self._recognition_threshold:

            return (
                "Unknown",
                best_similarity,
            )

        return (
            best_identity,
            best_similarity,
        )

    def recognize(
        self,
        image: Any,
    ) -> list[dict]:
        """
        Recognizes every detected face.
        """

        if not self._loaded:
            raise RuntimeError(
                "Face Engine is not loaded."
            )

        faces = self.detect_faces(image)

        results = []

        for face in faces:

            embedding = self.generate_embedding(face)

            identity, confidence = self.compare_embedding(
                embedding
            )

            self._faces_processed += 1

            if identity == "Unknown":
                self._unknown_faces += 1
            else:
                self._known_faces += 1

            results.append(
                {
                    "identity": identity,
                    "confidence": confidence,
                    "bbox": face.bbox.tolist(),
                }
            )

        return results
    
    def statistics(self) -> dict:
        """
        Returns runtime statistics for the Face Engine.
        """

        return {
            "loaded": self._loaded,
            "identities": self._dataset.identity_count,
            "images": self._dataset.image_count,
            "faces_processed": self._faces_processed,
            "known_faces": self._known_faces,
            "unknown_faces": self._unknown_faces,
            "recognition_threshold": self._recognition_threshold,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"loaded={self._loaded}, "
            f"identities={self._dataset.identity_count})"
        )
    
    @property
    def cache_exists(self) -> bool:
        """
        Returns whether an embedding cache exists.
        """

        return self._cache_file.exists()
    
    @property
    def faces_processed(self) -> int:
        """
        Total number of faces processed since the engine was loaded.
        """
        return self._faces_processed


    @property
    def known_faces(self) -> int:
        """
        Total number of recognized faces.
        """
        return self._known_faces


    @property
    def unknown_faces(self) -> int:
        """
        Total number of unknown faces.
        """
        return self._unknown_faces
    
    def reset_statistics(self) -> None:
        """
        Resets all runtime statistics.
        """

        self._faces_processed = 0
        self._known_faces = 0
        self._unknown_faces = 0

        logger.info(
            "Face Engine statistics reset."
        )
    
