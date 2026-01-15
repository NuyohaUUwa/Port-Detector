"""
Localhost-only ports view.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QComboBox,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from src.ui.styles import Colors


class LocalhostPortsView(QWidget):
    """Table view filtered to localhost connections."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Filter Bar
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索端口、进程名...")
        self.search_input.textChanged.connect(self._apply_filter)
        filter_layout.addWidget(self.search_input, stretch=1)

        self.proto_combo = QComboBox()
        self.proto_combo.addItems(["全部协议", "TCP", "UDP"])
        self.proto_combo.currentTextChanged.connect(self._apply_filter)
        self.proto_combo.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {Colors.BG_DARK};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 5px 10px;
                color: {Colors.TEXT_MAIN};
            }}
            QComboBox::drop-down {{ border: none; }}
        """
        )
        filter_layout.addWidget(self.proto_combo)

        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["协议", "本地地址", "远程地址", "状态", "PID", "进程名"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        # Status Bar
        self.status_label = QLabel("0 条记录")
        self.status_label.setStyleSheet(
            f"color: {Colors.TEXT_MUTED}; font-size: 12px;"
        )
        layout.addWidget(self.status_label)

        self.all_connections = []

    def update_data(self, connections):
        """Receive full list, filter to localhost only, then apply UI filters."""
        self.all_connections = connections
        self._apply_filter()

    def _apply_filter(self):
        search_text = self.search_input.text().lower()
        proto_filter = self.proto_combo.currentText()

        filtered = []
        for conn in self.all_connections:
            # Localhost filter
            if conn.local_addr not in {"127.0.0.1", "::1", "localhost"}:
                continue

            # Protocol filter
            if proto_filter != "全部协议" and conn.protocol != proto_filter:
                continue

            # Search filter
            if search_text:
                searchable = (
                    f"{conn.local_addr}:{conn.local_port} "
                    f"{conn.remote_addr}:{conn.remote_port} "
                    f"{conn.process_name} {conn.status}"
                ).lower()
                if search_text not in searchable:
                    continue

            filtered.append(conn)

        self._populate_table(filtered)

    def _populate_table(self, connections):
        self.table.setRowCount(len(connections))
        self.status_label.setText(f"{len(connections)} 条记录")

        for row, conn in enumerate(connections):
            # Protocol
            item_proto = QTableWidgetItem(conn.protocol)
            if conn.protocol == "TCP":
                item_proto.setForeground(QColor(Colors.PRIMARY))
            else:
                item_proto.setForeground(QColor(Colors.SUCCESS))
            self.table.setItem(row, 0, item_proto)

            # Local Addr
            self.table.setItem(row, 1, QTableWidgetItem(f"{conn.local_addr}:{conn.local_port}"))

            # Remote Addr
            remote = f"{conn.remote_addr}:{conn.remote_port}" if conn.remote_addr else "-"
            self.table.setItem(row, 2, QTableWidgetItem(remote))

            # Status
            item_status = QTableWidgetItem(conn.status)
            if conn.status == "LISTEN":
                item_status.setForeground(QColor(Colors.SUCCESS))
            elif conn.status == "ESTABLISHED":
                item_status.setForeground(QColor(Colors.SECONDARY))
            else:
                item_status.setForeground(QColor(Colors.TEXT_MUTED))
            self.table.setItem(row, 3, item_status)

            # PID
            self.table.setItem(row, 4, QTableWidgetItem(str(conn.pid)))

            # Process Name
            self.table.setItem(row, 5, QTableWidgetItem(conn.process_name))
