"""
Main Application Window
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from src.ui.styles import Styles, Colors
from src.ui.widgets.sidebar import Sidebar
from src.ui.views.dashboard import DashboardView
from src.ui.views.port_table import PortTableView
from src.ui.views.localhost_ports import LocalhostPortsView
from src.ui.worker import ScanWorker
from src.core.ports import get_free_ports

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Port Detector Pro")
        self.resize(1280, 820)
        self.setMinimumSize(1100, 700)
        
        # Central Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        layout.addWidget(self.sidebar)
        
        # Content Area (Stacked Widget)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Views
        self.view_dashboard = DashboardView()
        self.view_table = PortTableView()
        self.view_localhost = LocalhostPortsView()
        
        self.stack.addWidget(self.view_dashboard)
        self.stack.addWidget(self.view_table)
        self.stack.addWidget(self.view_localhost)
        
        # Worker Thread
        self.worker = ScanWorker()
        self.worker.data_ready.connect(self._on_data_ready)
        self.worker.start()
        
        # Sidebar Control Connections
        self.sidebar.btn_toggle.clicked.connect(self._toggle_monitoring)
        self.sidebar.btn_refresh.clicked.connect(self.worker.force_scan)
        self.sidebar.query_free_ports.connect(self._on_query_free_ports)
        self.sidebar.query_localhost.connect(lambda: self._switch_page(2))
        
        # Apply Styles
        self.setStyleSheet(Styles.QSS)
        
    def _switch_page(self, index):
        self.stack.setCurrentIndex(index)
        
    def _on_data_ready(self, connections):
        # Update both views with new data
        self.view_dashboard.update_data(connections)
        self.view_table.update_data(connections)
        self.view_localhost.update_data(connections)
        
    def _toggle_monitoring(self):
        # Sidebar button text is already updated by sidebar itself
        # We just need to handle logic
        if self.sidebar.is_monitoring:
            self.view_dashboard.set_monitoring(True)
            if not self.worker.isRunning():
                self.worker.start()
            self.worker.is_running = True
        else:
            self.view_dashboard.set_monitoring(False)
            self.worker.stop()

    def _on_query_free_ports(self):
        try:
            ports = get_free_ports(count=5, min_port=1024, max_port=65535)
            if not ports:
                self._show_message(
                    icon=QMessageBox.Icon.Warning,
                    title="查询空白端口",
                    text="未能找到空闲端口，请稍后重试。"
                )
                return
            ports_text = "\n".join(f"• {p}" for p in ports)
            self._show_message(
                icon=QMessageBox.Icon.Information,
                title="查询空白端口",
                text="找到 5 个可用端口",
                info=f"可用端口（localhost）：\n{ports_text}"
            )
        except Exception as exc:
            self._show_message(
                icon=QMessageBox.Icon.Critical,
                title="查询空白端口",
                text="查询失败",
                info=str(exc)
            )

    def _show_message(self, icon: QMessageBox.Icon, title: str, text: str, info: str | None = None):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(text)
        if info:
            msg.setInformativeText(info)
        msg.setStyleSheet(
            f"""
            QMessageBox {{
                background-color: {Colors.BG_DARK};
                color: {Colors.TEXT_MAIN};
            }}
            QLabel {{
                color: {Colors.TEXT_MAIN};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: {Colors.BG_DARKER};
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.SECONDARY};
            }}
            """
        )
        msg.exec()
            
    def closeEvent(self, event):
        self.worker.stop()
        super().closeEvent(event)
