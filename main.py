"""
Application Entry Point
-----------------------
Starts the AI Multimodal Communication System.
"""

from src.core.app import Application
from src.core.logger import logger


def main():
    logger.info("Launching AI Multimodal Communication System")

    app = Application()

    app.run()


if __name__ == "__main__":
    main()