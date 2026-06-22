from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)


class ChatPanelWidget(QFrame):
    """
    AI Conversation Panel.

    This widget will eventually contain:
        - User conversation
        - AI responses
        - Speech transcription
        - Translation
        - Streaming LLM output
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_widgets()
        self._create_layout()
        self._apply_styles()

    def _create_widgets(self):

        self.title_label = QLabel("AI Conversation")

        self.chat_area = QTextEdit()

        self.chat_area.setReadOnly(True)

        self.chat_area.setPlainText(
            "AI Assistant Ready...\n\n"
            "Conversation history will appear here."
        )

    def _create_layout(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)

        layout.setSpacing(15)

        layout.addWidget(self.title_label)

        layout.addWidget(self.chat_area)

    def _apply_styles(self):

        self.setFrameShape(QFrame.StyledPanel)

        self.setFrameShadow(QFrame.Raised)

        title_font = QFont()

        title_font.setPointSize(12)

        title_font.setBold(True)

        self.title_label.setFont(title_font)

        self.title_label.setAlignment(Qt.AlignCenter)

        self.title_label.setObjectName("chatTitle")

        self.chat_area.setObjectName("chatArea")