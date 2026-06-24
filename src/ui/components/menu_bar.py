"""
Application Menu Bar
--------------------
Defines the application's main menu bar.
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar
from src.ai.managers.model_manager import ModelManager
#from core.logger import logger
from src.core.logger import logger

class AppMenuBar(QMenuBar):
    """
    Main application menu bar.
    """

    def __init__( 
        self,
        model_manager,
        parent=None,
    ):
        super().__init__(parent)
        self._model_manager = ModelManager()

        self._model_actions = {}
        
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

        for model_name in self._model_manager.list_models():

            action = QAction(model_name, self)

            action.triggered.connect(
                lambda checked=False, name=model_name:
                self._load_model(name)
            )

            self._model_actions[model_name] = action

            models_menu.addAction(action)

        models_menu.addSeparator()

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

    def _load_model(self, model_name: str):
        """
        Load the selected AI model.
        """

        try:

            active_model = self._model_manager.active_model

            if (
                active_model is not None
                and active_model.model_name != model_name
            ):
                self._model_manager.unload_model(
                    active_model.model_name
                )

            self._model_manager.load_model(model_name)

            if self.parent():

                self.parent().ai_worker.set_model(model_name)

                self.parent().header.set_model_status(
                    model_name
                )

                self.parent().status_bar.showMessage(
                    f"AI Model Loaded : {model_name}"
                )

            logger.info(
                f"Loaded AI Model : {model_name}"
            )

        except Exception as e:

            logger.error(str(e))

            if self.parent():

                self.parent().status_bar.showMessage(
                    str(e)
                )