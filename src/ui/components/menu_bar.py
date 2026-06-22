"""
Application Menu Bar
--------------------
Defines the application's main menu bar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar

#from core.logger import logger
from src.core.logger import logger

class AppMenuBar(QMenuBar):
    """
    Main application menu bar.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info("Creating Menu Bar")

        self._create_actions()
        self._create_menus()
        self._connect_signals()

        logger.info("Menu Bar Created Successfully")

    def _create_actions(self):
        """
        Create every QAction used by the menu.
        """

        # File
        self.open_image_action = QAction("Open Image", self)
        self.open_video_action = QAction("Open Video", self)
        self.save_session_action = QAction("Save Session", self)
        self.export_action = QAction("Export", self)
        self.exit_action = QAction("Exit", self)

        # View
        self.toggle_fullscreen_action = QAction("Toggle Fullscreen", self)

        # Tools
        self.preferences_action = QAction("Preferences", self)

        # Models
        self.manage_models_action = QAction("Manage Models", self)

        # Settings
        self.application_settings_action = QAction(
            "Application Settings",
            self,
        )

        # Help
        self.documentation_action = QAction("Documentation", self)
        self.about_action = QAction("About", self)

    def _create_menus(self):
        """
        Create the menu hierarchy.
        """

        file_menu = self.addMenu("File")

        file_menu.addAction(self.open_image_action)
        file_menu.addAction(self.open_video_action)

        file_menu.addSeparator()

        file_menu.addAction(self.save_session_action)
        file_menu.addAction(self.export_action)

        file_menu.addSeparator()

        file_menu.addAction(self.exit_action)

        view_menu = self.addMenu("View")
        view_menu.addAction(self.toggle_fullscreen_action)

        tools_menu = self.addMenu("Tools")
        tools_menu.addAction(self.preferences_action)

        models_menu = self.addMenu("Models")
        models_menu.addAction(self.manage_models_action)

        settings_menu = self.addMenu("Settings")
        settings_menu.addAction(
            self.application_settings_action
        )

        help_menu = self.addMenu("Help")
        help_menu.addAction(self.documentation_action)

        help_menu.addSeparator()

        help_menu.addAction(self.about_action)

    def _connect_signals(self):
        """
        Connect actions.

        Functionality will be implemented in future milestones.
        """

        if self.parent():
            self.exit_action.triggered.connect(
                self.parent().close
            )