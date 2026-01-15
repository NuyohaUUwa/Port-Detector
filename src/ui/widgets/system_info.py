"""
System Info Card - 本机信息 + Port Detector 运行状态
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from src.ui.styles import Colors


class InfoRow(QFrame):
    """信息行：左文字 + 右值"""

    def __init__(self, label: str, value: str = "-", parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(6)

        self.lbl_label = QLabel(label)
        self.lbl_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 12px;")
        layout.addWidget(self.lbl_label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {Colors.TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(self.lbl_value, 0, 1, Qt.AlignmentFlag.AlignRight)

    def set_value(self, value: str):
        self.lbl_value.setText(value)


class SystemInfoCard(QFrame):
    """
    显示本机网络信息 + Port Detector 自身占用
    调用 update_data(data: dict) 更新
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        title = QLabel("本机信息 & 运行状态")
        title.setStyleSheet(f"color: {Colors.TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # 信息行
        self.row_ip = InfoRow("本机 IP")
        self.row_host = InfoRow("主机名")
        self.row_monitor = InfoRow("监控状态")
        self.row_last_scan = InfoRow("上次扫描")
        self.row_cpu = InfoRow("CPU 占用")
        self.row_mem = InfoRow("内存占用")
        self.row_uptime = InfoRow("运行时长")

        for row in [
            self.row_ip,
            self.row_host,
            self.row_monitor,
            self.row_last_scan,
            self.row_cpu,
            self.row_mem,
            self.row_uptime,
        ]:
            layout.addWidget(row)

        layout.addStretch()

    def update_data(self, info: dict):
        """
        info keys:
          ip, hostname, monitoring(bool), last_scan(str),
          cpu_percent(float), mem_mb(float), uptime(str)
        """
        self.row_ip.set_value(info.get("ip", "-"))
        self.row_host.set_value(info.get("hostname", "-"))

        monitoring = info.get("monitoring", False)
        monitor_text = "运行中" if monitoring else "已暂停"
        self.row_monitor.set_value(monitor_text)

        self.row_last_scan.set_value(info.get("last_scan", "-"))

        cpu = info.get("cpu_percent", None)
        cpu_text = f"{cpu:.1f}%" if cpu is not None else "-"
        self.row_cpu.set_value(cpu_text)

        mem = info.get("mem_mb", None)
        mem_text = f"{mem:.1f} MB" if mem is not None else "-"
        self.row_mem.set_value(mem_text)

        self.row_uptime.set_value(info.get("uptime", "-"))
