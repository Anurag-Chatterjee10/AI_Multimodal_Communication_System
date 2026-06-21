"""
Application Controller
----------------------
Initializes and manages the application.
"""

from PySide6.QtWidgets import QApplication

from src.core.logger import logger
from src.ui.main_window import MainWindow


class Application:
    """
    Main application controller.
    """

    def __init__(self):
        logger.info("Creating Application")

        self.qt_app = QApplication([])

        self.window = MainWindow()

    def run(self):
        """
        Start the application.
        """

        logger.info("Starting Application")

        self.window.show()

        self.qt_app.exec()