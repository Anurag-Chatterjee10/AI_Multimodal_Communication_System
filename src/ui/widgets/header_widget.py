from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)


class HeaderWidget(QWidget):
    """
    Professional application header.

    Displays:
        • Project title
        • Subtitle
        • AI model status
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()
        self._apply_styles()

    def _create_widgets(self):
        self.title_label = QLabel("AI Multimodal Communication System")

        self.subtitle_label = QLabel(
            "Intelligent Multimodal AI Desktop Platform"
        )

        self.status_label = QLabel("● AI Model : Not Loaded")

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(8)

        self.title_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        status_layout = QHBoxLayout()
        status_layout.addStretch()
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addLayout(status_layout)

    def _apply_styles(self):
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)

        subtitle_font = QFont()
        subtitle_font.setPointSize(10)

        status_font = QFont()
        status_font.setPointSize(10)
        status_font.setBold(True)

        self.title_label.setFont(title_font)
        self.subtitle_label.setFont(subtitle_font)
        self.status_label.setFont(status_font)

        self.title_label.setObjectName("headerTitle")
        self.subtitle_label.setObjectName("headerSubtitle")
        self.status_label.setObjectName("headerStatus")

    def set_model_status(
            self,
            model_name: str,
        ):
            """
            Update the currently loaded AI model.
            """

            self.status_label.setText(
                f"● AI Model : {model_name}"
            )