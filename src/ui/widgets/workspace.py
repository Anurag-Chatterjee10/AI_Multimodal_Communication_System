from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from .panels.camera_panel_widget import CameraPanelWidget
from .panels.chat_panel_widget import ChatPanelWidget
from .panels.control_panel_widget import ControlPanelWidget
from .panels.output_panel_widget import OutputPanelWidget


class Workspace(QWidget):
    """
    Main application workspace.

    Responsible only for arranging the
    major UI panels.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):

        self.camera_panel = CameraPanelWidget()

        self.chat_panel = ChatPanelWidget()

        self.control_panel = ControlPanelWidget()

        self.output_panel = OutputPanelWidget()

    def _create_layout(self):

        layout = QGridLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)

        layout.setHorizontalSpacing(15)

        layout.setVerticalSpacing(15)

        layout.addWidget(self.camera_panel, 0, 0)

        layout.addWidget(self.chat_panel, 0, 1)

        layout.addWidget(self.control_panel, 1, 0)

        layout.addWidget(self.output_panel, 1, 1)

        layout.setColumnStretch(0, 1)

        layout.setColumnStretch(1, 2)

        layout.setRowStretch(0, 3)

        layout.setRowStretch(1, 1)