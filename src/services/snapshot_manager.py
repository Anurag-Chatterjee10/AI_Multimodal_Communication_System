"""
Snapshot Manager
----------------

Handles saving camera frames as image files.
"""

from pathlib import Path
from datetime import datetime

import cv2

from src.core.logger import logger


class SnapshotManager:
    """
    Save snapshots from OpenCV frames.
    """

    EXPORT_DIRECTORY = Path("exports/images")

    @classmethod
    def save_snapshot(cls, frame):
        """
        Save a snapshot.

        Parameters
        ----------
        frame
            OpenCV frame.

        Returns
        -------
        Path
            Saved image path.
        """

        cls.EXPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = datetime.now().strftime(
            "snapshot_%Y%m%d_%H%M%S.png"
        )

        filepath = cls.EXPORT_DIRECTORY / filename

        cv2.imwrite(
            str(filepath),
            frame,
        )

        logger.info(
            f"Snapshot saved : {filepath}"
        )

        return filepath