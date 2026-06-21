"""
Main Application Window
-----------------------
Creates the main GUI window.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)

from src.config import settings
from src.config import constants
from src.core.logger import logger
from src.ui.theme import DARK_THEME


class MainWindow(QMainWindow):
    """
    Main window of the application.
    """

    def __init__(self):
        super().__init__()

        logger.info("Initializing Main Window")

        self.setup_window()
        self.create_ui()

    def setup_window(self):
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

    def create_ui(self):
        """
        Create the user interface.
        """

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        central_widget.setLayout(layout)

        title = QLabel("AI Multimodal Communication System")

        layout.addWidget(title)

        logger.info("Main Window Created Successfully")