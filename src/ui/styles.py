"""
UI Styles and Theme Configuration
"""

class Colors:
    # Main Backgrounds
    BG_DARK = "#1E1E2E"
    BG_DARKER = "#181825"
    BG_CARD = "#313244"
    
    # Accents
    PRIMARY = "#89B4FA"
    SECONDARY = "#B4BEFE"
    SUCCESS = "#A6E3A1"
    WARNING = "#F9E2AF"
    ERROR = "#F38BA8"
    
    # Text
    TEXT_MAIN = "#CDD6F4"
    TEXT_MUTED = "#A6ADC8"
    
    # Borders
    BORDER = "#45475A"

class Styles:
    QSS = f"""
    QMainWindow {{
        background-color: {Colors.BG_DARKER};
    }}
    
    QWidget {{
        color: {Colors.TEXT_MAIN};
        font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
        font-size: 14px;
    }}
    
    /* QFrame & Cards */
    QFrame#Card {{
        background-color: {Colors.BG_CARD};
        border-radius: 10px;
        border: 1px solid {Colors.BORDER};
    }}
    
    QFrame#Sidebar {{
        background-color: {Colors.BG_DARK};
        border-right: 1px solid {Colors.BORDER};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {Colors.PRIMARY};
        color: {Colors.BG_DARKER};
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {Colors.SECONDARY};
    }}
    
    QPushButton:pressed {{
        background-color: {Colors.PRIMARY};
        margin-top: 1px;
    }}
    
    QPushButton#SecondaryBtn {{
        background-color: {Colors.BG_CARD};
        color: {Colors.TEXT_MAIN};
        border: 1px solid {Colors.BORDER};
    }}
    
    QPushButton#SecondaryBtn:hover {{
        background-color: {Colors.BORDER};
    }}
    
    /* Table Widget */
    QTableWidget {{
        background-color: {Colors.BG_CARD};
        border: 1px solid {Colors.BORDER};
        border-radius: 8px;
        gridline-color: {Colors.BORDER};
        selection-background-color: {Colors.PRIMARY};
        selection-color: {Colors.BG_DARKER};
    }}
    
    QTableWidget::item {{
        padding: 5px;
    }}
    
    QHeaderView::section {{
        background-color: {Colors.BG_DARK};
        color: {Colors.TEXT_MUTED};
        padding: 8px;
        border: none;
        border-bottom: 1px solid {Colors.BORDER};
        font-weight: bold;
    }}
    
    QTableCornerButton::section {{
        background-color: {Colors.BG_DARK};
        border: none;
    }}
    
    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: {Colors.BG_DARK};
        width: 10px;
        margin: 0px 0px 0px 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {Colors.BORDER};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    /* Search Input */
    QLineEdit {{
        background-color: {Colors.BG_DARK};
        border: 1px solid {Colors.BORDER};
        border-radius: 6px;
        padding: 6px 12px;
        color: {Colors.TEXT_MAIN};
    }}
    QLineEdit:focus {{
        border: 1px solid {Colors.PRIMARY};
    }}
    """
