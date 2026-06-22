from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFont,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class CameraPanelWidget(QFrame):
    """
    Camera panel.

    Responsible ONLY for displaying
    camera frames.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()

        self._create_layout()

        self._apply_styles()

    # =======================================================
    # UI
    # =======================================================

    def _create_widgets(self):

        self.title_label = QLabel("Camera Feed")

        self.preview_label = QLabel(
            "No Camera Connected"
        )

    def _create_layout(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        layout.setSpacing(15)

        layout.addWidget(self.title_label)

        layout.addWidget(
            self.preview_label,
            1,
        )

    def _apply_styles(self):

        self.setFrameShape(QFrame.StyledPanel)

        self.setFrameShadow(QFrame.Raised)

        title_font = QFont()

        title_font.setPointSize(12)

        title_font.setBold(True)

        self.title_label.setFont(title_font)

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.preview_label.setAlignment(
            Qt.AlignCenter
        )

        self.preview_label.setObjectName(
            "cameraPlaceholder"
        )

        self.title_label.setObjectName(
            "cameraTitle"
        )

    # =======================================================
    # Public API
    # =======================================================

    def set_frame(self, pixmap: QPixmap):
        """
        Display the latest camera frame.
        """

        scaled = pixmap.scaled(
            self.preview_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.preview_label.setPixmap(
            scaled
        )