"""
Main Application Window
-----------------------
Assembles the application's GUI.
"""

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

from src.config import settings
from src.config import constants

from src.core.logger import logger

from src.services.camera_service import CameraService
from src.controllers.app_controller import AppController

from src.ui.theme import DARK_THEME

from src.ui.components.menu_bar import AppMenuBar
from src.ui.components.tool_bar import AppToolBar
from src.ui.components.status_bar import AppStatusBar

from src.ui.widgets.header_widget import HeaderWidget
from src.ui.widgets.workspace import Workspace


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        logger.info("Initializing Main Window")

        self._setup_window()

        self._create_components()

        self._create_layout()

        self.controller = AppController(
            self,
            self.camera_service,
        )

        logger.info("Main Window Created Successfully")

    def _setup_window(self):
        """
        Configure the main window.
        """

        self.setWindowTitle(constants.APP_NAME)

        self.resize(
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT,
        )

        self.setMinimumSize(
            settings.WINDOW_MIN_WIDTH,
            settings.WINDOW_MIN_HEIGHT,
        )

        self.setStyleSheet(DARK_THEME)

    def _create_components(self):
        """
        Create reusable GUI components.
        """

        self.menu_bar = AppMenuBar(self)

        self.tool_bar = AppToolBar(self)

        self.status_bar = AppStatusBar(self)

        self.header = HeaderWidget()

        self.workspace = Workspace()

        self.camera_service = CameraService()

    def _create_layout(self):
        """
        Assemble the application.
        """

        self.setMenuBar(self.menu_bar)

        self.addToolBar(self.tool_bar)

        self.setStatusBar(self.status_bar)

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        central_widget.setLayout(layout)

        layout.addWidget(self.header)

        layout.addWidget(self.workspace)

    def closeEvent(self, event: QCloseEvent):
        """
        Gracefully shutdown application.
        """

        self.controller.recording_manager.shutdown()

        self.camera_service.stop()

        event.accept()