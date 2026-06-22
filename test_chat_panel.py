import sys

from PySide6.QtWidgets import QApplication

from src.ui.widgets.panels.chat_panel_widget import ChatPanelWidget


def main():

    app = QApplication(sys.argv)

    window = ChatPanelWidget()

    window.resize(700, 500)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()