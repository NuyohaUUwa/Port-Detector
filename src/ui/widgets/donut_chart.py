"""
Custom Donut Chart Widget
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt, QRectF
from src.ui.styles import Colors

class DonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 240)
        self.tcp_count = 0
        self.udp_count = 0
        
    def update_data(self, tcp: int, udp: int):
        self.tcp_count = tcp
        self.udp_count = udp
        self.update()  # Trigger repaint
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensions
        width = self.width()
        height = self.height()
        size = min(width, height)
        margin = 20
        rect = QRectF((width - size)/2 + margin, (height - size)/2 + margin, 
                      size - 2*margin, size - 2*margin)
        
        total = self.tcp_count + self.udp_count
        
        # Draw background track
        pen_width = 25
        painter.setPen(QPen(QColor(Colors.BG_DARK), pen_width, Qt.PenStyle.SolidLine))
        painter.drawEllipse(rect)
        
        # Draw arcs
        if total > 0:
            start_angle = 90 * 16
            
            # TCP Arc
            if self.tcp_count > 0:
                span = int(-(self.tcp_count / total) * 360 * 16)
                painter.setPen(QPen(QColor(Colors.PRIMARY), pen_width, Qt.PenStyle.SolidLine))
                painter.drawArc(rect, start_angle, span)
                start_angle += span
            
            # UDP Arc
            if self.udp_count > 0:
                span = int(-(self.udp_count / total) * 360 * 16)
                painter.setPen(QPen(QColor(Colors.SUCCESS), pen_width, Qt.PenStyle.SolidLine))
                painter.drawArc(rect, start_angle, span)
        else:
            # Draw empty ring
            painter.setPen(QPen(QColor(Colors.BORDER), pen_width, Qt.PenStyle.SolidLine))
            painter.drawEllipse(rect)
            
        # Draw Center Text
        painter.setPen(QColor(Colors.TEXT_MAIN))
        font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(total))
        
        font_sub = QFont("Segoe UI", 10)
        painter.setFont(font_sub)
        
        # Offset for subtitle
        sub_rect = QRectF(rect.x(), rect.y() + 25, rect.width(), rect.height())
        painter.setPen(QColor(Colors.TEXT_MUTED))
        painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, "连接")
