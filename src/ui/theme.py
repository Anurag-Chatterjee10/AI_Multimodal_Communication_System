"""
Application Theme
-----------------
Contains the application's centralized theme.
"""

from PySide6.QtGui import QFont

# ==========================================================
# Colors
# ==========================================================

BACKGROUND_COLOR = "#202124"

SURFACE_COLOR = "#303134"

BUTTON_COLOR = "#3C4043"

BUTTON_HOVER_COLOR = "#5F6368"

TEXT_COLOR = "#FFFFFF"

BORDER_COLOR = "#5F6368"

# ==========================================================
# Fonts
# ==========================================================

TITLE_FONT = QFont(
    "Segoe UI",
    18,
    QFont.Bold,
)

HEADING_FONT = QFont(
    "Segoe UI",
    14,
    QFont.Bold,
)

BODY_FONT = QFont(
    "Segoe UI",
    11,
)

STATUS_FONT = QFont(
    "Segoe UI",
    10,
)

# ==========================================================
# Application Stylesheet
# ==========================================================

DARK_THEME = f"""
QMainWindow {{
    background-color: {BACKGROUND_COLOR};
}}

QWidget {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
    font-size: 14px;
    font-family: Segoe UI;
}}

QPushButton {{
    background-color: {BUTTON_COLOR};
    color: {TEXT_COLOR};
    border: none;
    border-radius: 6px;
    padding: 8px;
}}

QPushButton:hover {{
    background-color: {BUTTON_HOVER_COLOR};
}}

QLineEdit {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 5px;
    padding: 5px;
}}

QMenuBar {{
    background-color: {BUTTON_COLOR};
}}

QMenuBar::item:selected {{
    background-color: {BUTTON_HOVER_COLOR};
}}

QToolBar {{
    background-color: {BUTTON_COLOR};
}}

QStatusBar {{
    background-color: {BUTTON_COLOR};
}}

QGroupBox {{
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    margin-top: 10px;
}}

QGroupBox::title {{
    left: 10px;
    padding: 0px 5px;
}}
"""