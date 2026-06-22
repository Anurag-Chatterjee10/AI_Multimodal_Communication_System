"""
Application Tool Bar
--------------------
Defines the application's main toolbar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

#from core.logger import logger
from src.core.logger import logger

class AppToolBar(QToolBar):
    """
    Main application toolbar.
    """

    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)

        logger.info("Creating Tool Bar")

        self.setMovable(False)

        self.setFloatable(False)

        self._create_actions()

        self._create_toolbar()

        self._connect_signals()

        logger.info("Tool Bar Created Successfully")

    def _create_actions(self):
        """
        Create toolbar actions.
        """

        self.camera_action = QAction("📷 Camera", self)

        self.microphone_action = QAction("🎤 Mic", self)

        self.open_action = QAction("📂 Open", self)

        self.save_action = QAction("💾 Save", self)

        self.start_action = QAction("▶ Start", self)

        self.stop_action = QAction("⏹ Stop", self)

    def _create_toolbar(self):
        """
        Populate the toolbar.
        """

        self.addAction(self.camera_action)

        self.addAction(self.microphone_action)

        self.addSeparator()

        self.addAction(self.open_action)

        self.addAction(self.save_action)

        self.addSeparator()

        self.addAction(self.start_action)

        self.addAction(self.stop_action)

    def _connect_signals(self):
        """
        Connect toolbar actions.

        Functionality will be added
        during future milestones.
        """

        pass