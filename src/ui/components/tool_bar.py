"""
Application Tool Bar
--------------------
Defines the application's main toolbar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

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

        # ------------------------------------------------------
        # Initial Toolbar State
        # ------------------------------------------------------

        self.set_recording_state(False)

        logger.info("Tool Bar Created Successfully")

    # ==========================================================
    # Actions
    # ==========================================================

    def _create_actions(self):
        """
        Create toolbar actions.
        """

        # ------------------------------------------------------
        # Device Controls
        # ------------------------------------------------------

        self.camera_action = QAction("📷 Camera", self)

        self.microphone_action = QAction("🎤 Mic", self)

        # ------------------------------------------------------
        # File Operations
        # ------------------------------------------------------

        self.open_action = QAction("📂 Open", self)

        self.save_action = QAction("💾 Save", self)

        # ------------------------------------------------------
        # Camera Controls
        # ------------------------------------------------------

        self.start_action = QAction("▶ Start", self)

        self.stop_action = QAction("⏹ Stop", self)

        # ------------------------------------------------------
        # Multimedia
        # ------------------------------------------------------

        self.snapshot_action = QAction("📸 Snapshot", self)

        self.record_action = QAction("⏺ Record", self)

        self.stop_record_action = QAction(
            "⏹ Stop Recording",
            self,
        )

        # ------------------------------------------------------
        # Application
        # ------------------------------------------------------

        self.settings_action = QAction("⚙ Settings", self)

    # ==========================================================
    # Toolbar Layout
    # ==========================================================

    def _create_toolbar(self):
        """
        Populate the toolbar.
        """

        # ------------------------------------------------------
        # Devices
        # ------------------------------------------------------

        self.addAction(self.camera_action)

        self.addAction(self.microphone_action)

        self.addSeparator()

        # ------------------------------------------------------
        # Files
        # ------------------------------------------------------

        self.addAction(self.open_action)

        self.addAction(self.save_action)

        self.addSeparator()

        # ------------------------------------------------------
        # Camera
        # ------------------------------------------------------

        self.addAction(self.start_action)

        self.addAction(self.stop_action)

        self.addSeparator()

        # ------------------------------------------------------
        # Multimedia
        # ------------------------------------------------------

        self.addAction(self.snapshot_action)

        self.addAction(self.record_action)

        self.addAction(self.stop_record_action)

        self.addSeparator()

        # ------------------------------------------------------
        # Application
        # ------------------------------------------------------

        self.addAction(self.settings_action)

    # ==========================================================
    # Recording State
    # ==========================================================

    def set_recording_state(self, recording: bool) -> None:
        """
        Update recording button states.

        Args:
            recording:
                True if recording is active.
        """

        self.record_action.setEnabled(not recording)

        self.stop_record_action.setEnabled(recording)

    # ==========================================================
    # Signal Connections
    # ==========================================================

    def _connect_signals(self):
        """
        Connect toolbar actions.

        Functionality will be added
        during future milestones.
        """

        pass