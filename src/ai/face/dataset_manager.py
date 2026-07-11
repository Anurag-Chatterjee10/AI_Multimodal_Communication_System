"""
Face Dataset Manager

Responsible for discovering and managing the
face recognition dataset.

Dataset Structure

datasets/
└── faces/
    ├── Person1/
    │   ├── image1.jpg
    │   ├── image2.png
    │   └── ...
    │
    ├── Person2/
    │   └── ...
"""

from pathlib import Path


class FaceDatasetManager:
    """
    Manages the complete face dataset.

    Responsibilities
    ----------------
    - Locate dataset
    - Validate structure
    - Enumerate identities
    - Enumerate images
    """

    VALID_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
    }

    def __init__(
        self,
        dataset_path: str = "datasets/faces",
    ):
        self._dataset_path = Path(dataset_path)

        self._identities: dict[str, list[Path]] = {}

    @property
    def dataset_path(self) -> Path:
        """
        Returns dataset location.
        """
        return self._dataset_path

    @property
    def identities(self) -> dict[str, list[Path]]:
        """
        Returns all identities.
        """
        return self._identities

    @property
    def identity_names(self) -> list[str]:
        """
        Returns all identity names.
        """
        return sorted(self._identities.keys())

    @property
    def identity_count(self) -> int:
        """
        Returns total identities.
        """
        return len(self._identities)

    def dataset_exists(self) -> bool:
        """
        Checks whether the dataset exists.
        """
        return self._dataset_path.exists()

    def clear(self) -> None:
        """
        Clears loaded dataset.
        """
        self._identities.clear()

    def load(self) -> None:
        """
        Loads the entire dataset.
        """

        self.clear()

        if not self.dataset_exists():
            raise FileNotFoundError(
                f"Dataset not found: {self._dataset_path}"
            )

        for person_dir in sorted(self._dataset_path.iterdir()):

            if not person_dir.is_dir():
                continue

            images = []

            for image in sorted(person_dir.iterdir()):

                if (
                    image.is_file()
                    and image.suffix.lower() in self.VALID_EXTENSIONS
                ):
                    images.append(image)

            if images:
                self._identities[person_dir.name] = images

    def get_images(
        self,
        identity: str,
    ) -> list[Path]:
        """
        Returns all images belonging
        to an identity.
        """

        return self._identities.get(identity, [])

    def total_images(self) -> int:
        """
        Returns total images.
        """

        return sum(
            len(images)
            for images in self._identities.values()
        )

    def summary(self) -> dict:
        """
        Returns dataset statistics.
        """

        return {
            "dataset": str(self._dataset_path),
            "identities": self.identity_count,
            "images": self.total_images(),
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"identities={self.identity_count}, "
            f"images={self.total_images()})"
        )
    
    @property
    def image_count(self) -> int:
        """
        Returns the total number of face images in the dataset.
        """

        return sum(
            len(images)
            for images in self._identities.values()
        )