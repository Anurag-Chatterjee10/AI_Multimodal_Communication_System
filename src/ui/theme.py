"""
Application Theme
-----------------
Contains the application's stylesheet.
"""


DARK_THEME = """
QMainWindow {
    background-color: #202124;
}

QWidget {
    background-color: #202124;
    color: white;
    font-size: 14px;
    font-family: Segoe UI;
}

QPushButton {
    background-color: #3C4043;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px;
}

QPushButton:hover {
    background-color: #5F6368;
}

QLineEdit {
    background-color: #303134;
    color: white;
    border: 1px solid #5F6368;
    border-radius: 5px;
    padding: 5px;
}
"""