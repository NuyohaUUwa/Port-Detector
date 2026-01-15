"""
Sidebar Navigation Widget
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from src.ui.styles import Colors

class Sidebar(QFrame):
    # Signals for page navigation
    page_changed = pyqtSignal(int)  # 0: Dashboard, 1: Port List
    query_localhost = pyqtSignal()
    query_free_ports = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 25, 15, 25)
        
        # App Title
        title = QLabel("⚡ Port Detector")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Colors.TEXT_MAIN};")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Navigation Buttons
        self.btn_dashboard = self._create_nav_btn("📊  仪表盘", 0)
        self.btn_ports = self._create_nav_btn("🔌  端口列表", 1)
        self.btn_localhost = self._create_nav_btn("🏠  localhost 端口", 2)
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_ports)
        layout.addWidget(self.btn_localhost)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Control Section
        lbl_control = QLabel("控制")
        lbl_control.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 12px; font-weight: bold;")
        layout.addWidget(lbl_control)
        
        self.btn_toggle = QPushButton("⏸  暂停监控")
        self.btn_toggle.clicked.connect(self._on_toggle)
        layout.addWidget(self.btn_toggle)
        
        self.btn_refresh = QPushButton("⟳  立即刷新")
        self.btn_refresh.setObjectName("SecondaryBtn")
        layout.addWidget(self.btn_refresh)

        self.btn_free_ports = QPushButton("🆕  查询空白端口")
        self.btn_free_ports.setObjectName("SecondaryBtn")
        self.btn_free_ports.clicked.connect(self.query_free_ports.emit)
        layout.addWidget(self.btn_free_ports)
        
        # Default state
        self.is_monitoring = True
        self._active_btn = self.btn_dashboard
        self._update_btn_style(self.btn_dashboard, True)
    
    def _create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setStyleSheet(self._get_btn_style(False))
        btn.clicked.connect(lambda: self._on_nav_click(btn, index))
        return btn
    
    def _on_nav_click(self, btn, index):
        if self._active_btn:
            self._active_btn.setChecked(False)
            self._update_btn_style(self._active_btn, False)
        
        btn.setChecked(True)
        self._active_btn = btn
        self._update_btn_style(btn, True)
        
        self.page_changed.emit(index)
        
    def _update_btn_style(self, btn, active):
        btn.setStyleSheet(self._get_btn_style(active))
        
    def _get_btn_style(self, active):
        if active:
            return f"""
                background-color: {Colors.PRIMARY};
                color: {Colors.BG_DARKER};
                text-align: left;
                padding-left: 15px;
            """
        else:
            return f"""
                background-color: transparent;
                color: {Colors.TEXT_MAIN};
                text-align: left;
                padding-left: 15px;
                border: none;
            """
            
    def _on_toggle(self):
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.btn_toggle.setText("⏸  暂停监控")
            self.btn_toggle.setStyleSheet(f"background-color: {Colors.WARNING}; color: {Colors.BG_DARKER};")
        else:
            self.btn_toggle.setText("▶  开始监控")
            self.btn_toggle.setStyleSheet(f"background-color: {Colors.SUCCESS}; color: {Colors.BG_DARKER};")
            
        # Signal handler will be connected in MainWindow
