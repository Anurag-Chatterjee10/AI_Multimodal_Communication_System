from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)


class OutputPanelWidget(QFrame):
    """
    Output Panel.

    Displays all AI generated output and
    application logs.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()
        self._apply_styles()

    def _create_widgets(self):

        self.title_label = QLabel("System Output")

        self.output_area = QTextEdit()

        self.output_area.setReadOnly(True)

        self.output_area.setPlainText(
            "Application Started...\n\n"
            "Waiting for AI modules..."
        )

    def _create_layout(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)

        layout.setSpacing(15)

        layout.addWidget(self.title_label)

        layout.addWidget(self.output_area)

    def _apply_styles(self):

        self.setFrameShape(QFrame.StyledPanel)

        self.setFrameShadow(QFrame.Raised)

        font = QFont()

        font.setPointSize(12)

        font.setBold(True)

        self.title_label.setFont(font)

        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setObjectName("outputTitle")

        self.output_area.setObjectName("outputArea")