"""
Application Status Bar
----------------------
Defines the application's main status bar.
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QStatusBar

#from core.logger import logger
from src.core.logger import logger

class AppStatusBar(QStatusBar):
    """
    Main application status bar.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Creating Status Bar")

        self._create_widgets()

        self._create_layout()

        logger.info("Status Bar Created Successfully")

    def _create_widgets(self):
        """
        Create all status labels.
        """

        self.ready_label = QLabel("Ready")

        self.camera_label = QLabel("Camera : Offline")

        self.microphone_label = QLabel("Microphone : Offline")

        self.ai_label = QLabel("AI : Not Loaded")

    def _create_layout(self):
        """
        Add labels to the status bar.
        """

        self.addWidget(self.ready_label)

        self.addPermanentWidget(self.camera_label)

        self.addPermanentWidget(self.microphone_label)

        self.addPermanentWidget(self.ai_label)

    # ----------------------------------------------------
    # Future Update Methods
    # ----------------------------------------------------

    def set_camera_status(self, status: str):
        self.camera_label.setText(f"Camera : {status}")

    def set_microphone_status(self, status: str):
        self.microphone_label.setText(f"Microphone : {status}")

    def set_ai_status(self, status: str):
        self.ai_label.setText(f"AI : {status}")

    def set_ready_message(self, message: str):
        self.ready_label.setText(message)