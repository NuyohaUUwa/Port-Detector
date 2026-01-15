"""
Top 10 Active Process List Widget
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QRectF
from src.ui.styles import Colors


class ProgressBar(QWidget):
    """简易水平进度条"""

    def __init__(self, value: int, maximum: int, parent=None):
        super().__init__(parent)
        self.value = value
        self.maximum = maximum if maximum > 0 else 1
        self.setFixedHeight(8)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # 背景
        bg_rect = QRectF(0, 0, width, height)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(Colors.BG_DARK)))
        painter.drawRoundedRect(bg_rect, 4, 4)

        # 进度
        if self.value > 0:
            ratio = min(self.value / self.maximum, 1.0)
            bar_w = max(width * ratio, 6)  # 确保最小可见宽度
            bar_rect = QRectF(0, 0, bar_w, height)
            painter.setBrush(QBrush(QColor(Colors.PRIMARY)))
            painter.drawRoundedRect(bar_rect, 4, 4)


class ProcessItem(QFrame):
    """单个进程条目"""

    def __init__(self, name: str, count: int, max_count: int, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 进程名
        self.lbl_name = QLabel()
        self.lbl_name.setFixedWidth(140)
        fm = self.lbl_name.fontMetrics()
        elided = fm.elidedText(name, Qt.TextElideMode.ElideRight, 130)
        self.lbl_name.setText(elided)
        self.lbl_name.setToolTip(name)
        self.lbl_name.setStyleSheet(f"color: {Colors.TEXT_MAIN}; font-size: 13px;")
        layout.addWidget(self.lbl_name)

        # 进度条
        self.progress = ProgressBar(count, max_count)
        layout.addWidget(self.progress, 1)

        # 数值
        self.lbl_count = QLabel(str(count))
        self.lbl_count.setFixedWidth(40)
        self.lbl_count.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_count.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-weight: bold;")
        layout.addWidget(self.lbl_count)


class ProcessList(QWidget):
    """活跃进程列表（Top 10）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def update_data(self, process_stats: list[tuple[str, int]]):
        """
        process_stats: [(process_name, count), ...]
        """
        # 清空
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not process_stats:
            lbl = QLabel("暂无活跃进程")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED}; padding: 20px;")
            self.layout.addWidget(lbl)
            return

        # 取前 10 项
        process_stats = process_stats[:10]
        max_count = max((cnt for _, cnt in process_stats), default=1)

        for name, count in process_stats:
            item = ProcessItem(name, count, max_count)
            self.layout.addWidget(item)

        self.layout.addStretch()
