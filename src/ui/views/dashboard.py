"""
Dashboard View
"""

import socket
import time
import platform

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from src.ui.styles import Colors
from src.ui.widgets.donut_chart import DonutChart
from src.ui.widgets.bar_chart import BarChart
from src.ui.widgets.process_list import ProcessList
from src.ui.widgets.system_info import SystemInfoCard
from src.core.scanner import (
    get_statistics,
    get_process_usage,
    get_self_usage,
)
import psutil


class StatCard(QFrame):
    def __init__(self, title, value="0", color=Colors.TEXT_MAIN, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 13px;")
        layout.addWidget(lbl_title)

        self.lbl_value = QLabel(str(value))
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.lbl_value)

    def set_value(self, value):
        self.lbl_value.setText(str(value))


class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.monitoring = True
        self.last_scan_time = "-"

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)
        # 让上排稍大、左右均衡
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 3)
        layout.setRowStretch(1, 2)

        # === 卡片 1: 协议分布甜甜圈 + 统计卡片 ===
        card_protocol = QFrame()
        card_protocol.setObjectName("Card")
        card_protocol.setMinimumHeight(360)
        lp = QVBoxLayout(card_protocol)
        lp.setContentsMargins(16, 16, 16, 16)
        lp.setSpacing(10)

        lbl_chart_title = QLabel("协议分布")
        lbl_chart_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_MAIN};")
        lp.addWidget(lbl_chart_title)

        self.chart = DonutChart()
        lp.addWidget(self.chart, alignment=Qt.AlignmentFlag.AlignCenter)

        # 统计卡片组
        stats_grid = QGridLayout()
        stats_grid.setSpacing(10)
        self.card_total = StatCard("总连接数", "0", Colors.TEXT_MAIN)
        self.card_tcp = StatCard("TCP 连接", "0", Colors.PRIMARY)
        self.card_udp = StatCard("UDP 连接", "0", Colors.SUCCESS)
        self.card_listen = StatCard("监听端口", "0", Colors.SUCCESS)
        self.card_est = StatCard("已建立连接", "0", Colors.SECONDARY)

        stats_grid.addWidget(self.card_total, 0, 0, 1, 2)
        stats_grid.addWidget(self.card_tcp, 1, 0)
        stats_grid.addWidget(self.card_udp, 1, 1)
        stats_grid.addWidget(self.card_listen, 2, 0)
        stats_grid.addWidget(self.card_est, 2, 1)
        lp.addLayout(stats_grid)

        layout.addWidget(card_protocol, 0, 0)

        # === 卡片 2: 状态分布条形图 ===
        card_status = QFrame()
        card_status.setObjectName("Card")
        card_status.setMinimumHeight(360)
        ls = QVBoxLayout(card_status)
        ls.setContentsMargins(16, 16, 16, 16)
        ls.setSpacing(10)

        lbl_status = QLabel("连接状态分布")
        lbl_status.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_MAIN};")
        ls.addWidget(lbl_status)

        self.bar_chart = BarChart()
        ls.addWidget(self.bar_chart)

        layout.addWidget(card_status, 0, 1)

        # === 卡片 3: 本机信息 + 运行占用 ===
        card_info = QFrame()
        card_info.setObjectName("Card")
        card_info.setMinimumHeight(300)
        li = QVBoxLayout(card_info)
        li.setContentsMargins(16, 16, 16, 16)
        li.setSpacing(12)

        self.system_info = SystemInfoCard()
        li.addWidget(self.system_info)

        layout.addWidget(card_info, 1, 0)

        # === 卡片 4: Top 活跃进程 ===
        card_proc = QFrame()
        card_proc.setObjectName("Card")
        card_proc.setMinimumHeight(300)
        lp2 = QVBoxLayout(card_proc)
        lp2.setContentsMargins(16, 16, 16, 16)
        lp2.setSpacing(10)

        lbl_proc = QLabel("Top 10 活跃进程（按连接数）")
        lbl_proc.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_MAIN};")
        lp2.addWidget(lbl_proc)

        self.proc_list = ProcessList()
        lp2.addWidget(self.proc_list)

        layout.addWidget(card_proc, 1, 1)

    def set_monitoring(self, monitoring: bool):
        self.monitoring = monitoring

    def update_data(self, connections):
        # 记录扫描时间
        self.last_scan_time = time.strftime("%H:%M:%S")

        # 统计
        stats = get_statistics(connections)
        status_counts = stats.get("status_counts", {})

        # 协议 & 数量
        self.card_total.set_value(stats.get("total", 0))
        self.card_tcp.set_value(stats.get("tcp", 0))
        self.card_udp.set_value(stats.get("udp", 0))
        self.card_listen.set_value(stats.get("listen", 0))
        self.card_est.set_value(stats.get("established", 0))
        self.chart.update_data(stats.get("tcp", 0), stats.get("udp", 0))

        # 状态分布
        self.bar_chart.update_data(status_counts)

        # 活跃进程
        proc_stats = get_process_usage(connections)
        self.proc_list.update_data(proc_stats)

        # 系统信息卡片
        self.system_info.update_data(self._build_system_info())

    def _build_system_info(self) -> dict:
        usage = get_self_usage()

        ip = self._get_primary_ip()
        hostname = socket.gethostname()

        return {
            "ip": ip,
            "hostname": hostname,
            "monitoring": self.monitoring,
            "last_scan": self.last_scan_time,
            "cpu_percent": usage.get("cpu_percent"),
            "mem_mb": usage.get("mem_mb"),
            "uptime": usage.get("uptime"),
        }

    def _get_primary_ip(self) -> str:
        """选择一个非回环 IPv4"""
        try:
            for _, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith(("127.", "169.254")):
                        return addr.address
        except Exception:
            pass
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "-"
