"""
Status Distribution Bar Chart (PyQt6)
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush
from PyQt6.QtCore import Qt, QRectF
from src.ui.styles import Colors


class BarChart(QWidget):
    """横向条形图，用于展示连接状态分布"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 220)
        self.data: dict[str, int] = {}

        # 状态显示顺序与颜色
        self.display_order = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "OTHER"]
        self.status_colors = {
            "LISTEN": Colors.SUCCESS,
            "ESTABLISHED": Colors.SECONDARY,
            "TIME_WAIT": Colors.WARNING,
            "CLOSE_WAIT": "#FAB387",  # 温和橙色
            "OTHER": "#6C7086",       # 中性灰
        }

    def update_data(self, status_counts: dict[str, int]):
        """更新状态统计数据"""
        self.data = status_counts or {}
        self.update()  # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        # 为标题和底部留白
        top_margin = 16
        left_label = 110
        right_value = 50
        bar_height = 22
        spacing = 14

        # 构建显示数据，合并其他状态为 OTHER
        items = []
        other_count = 0
        for status in self.display_order:
            if status == "OTHER":
                continue
            count = self.data.get(status, 0)
            if count > 0:
                items.append((status, count))
        for status, count in self.data.items():
            if status not in self.display_order:
                other_count += count
        if other_count > 0:
            items.append(("OTHER", other_count))

        # 最大值用于比例
        max_val = max((cnt for _, cnt in items), default=1)
        chart_width = max(width - left_label - right_value - 20, 50)

        font_label = QFont("Segoe UI", 9)
        font_value = QFont("Segoe UI", 9, QFont.Weight.Bold)

        y = top_margin
        for status, count in items:
            color = self.status_colors.get(status, Colors.TEXT_MUTED)

            # Label
            painter.setFont(font_label)
            painter.setPen(QColor(Colors.TEXT_MUTED))
            painter.drawText(
                0,
                y,
                left_label - 8,
                bar_height,
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                status,
            )

            # 背景条
            bg_rect = QRectF(left_label, y, chart_width, bar_height)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(Colors.BG_DARK)))
            painter.drawRoundedRect(bg_rect, 5, 5)

            # 进度条
            bar_w = (count / max_val) * chart_width if max_val > 0 else 0
            if count > 0:
                bar_w = max(bar_w, 6)  # 确保最小可见宽度
                bar_rect = QRectF(left_label, y, bar_w, bar_height)
                painter.setBrush(QBrush(QColor(color)))
                painter.drawRoundedRect(bar_rect, 5, 5)

            # 数值
            painter.setFont(font_value)
            painter.setPen(QColor(Colors.TEXT_MAIN))
            painter.drawText(
                left_label + chart_width + 6,
                y,
                right_value,
                bar_height,
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                str(count),
            )

            y += bar_height + spacing

        if not items:
            painter.setPen(QColor(Colors.TEXT_MUTED))
            painter.setFont(font_value)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "暂无数据")
