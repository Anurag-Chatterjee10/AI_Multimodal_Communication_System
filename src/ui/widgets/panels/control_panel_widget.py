from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
)


class ControlPanelWidget(QFrame):
    """
    Control Panel.

    This widget will eventually contain controls for:
    - Camera
    - Microphone
    - AI Model
    - Recording
    - Translation
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()
        self._apply_styles()

    def _create_widgets(self):

        self.title_label = QLabel("Controls")

        self.start_button = QPushButton("▶ Start")

        self.stop_button = QPushButton("⏹ Stop")

        self.camera_button = QPushButton("📷 Camera")

        self.mic_button = QPushButton("🎤 Microphone")

        buttons = [
            self.start_button,
            self.stop_button,
            self.camera_button,
            self.mic_button,
        ]

        for button in buttons:
            button.setEnabled(False)

    def _create_layout(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(15, 15, 15, 15)

        main_layout.setSpacing(15)

        grid = QGridLayout()

        grid.addWidget(self.start_button, 0, 0)
        grid.addWidget(self.stop_button, 0, 1)
        grid.addWidget(self.camera_button, 1, 0)
        grid.addWidget(self.mic_button, 1, 1)

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(grid)

    def _apply_styles(self):

        self.setFrameShape(QFrame.StyledPanel)

        self.setFrameShadow(QFrame.Raised)

        font = QFont()

        font.setPointSize(12)

        font.setBold(True)

        self.title_label.setFont(font)

        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setObjectName("controlTitle")