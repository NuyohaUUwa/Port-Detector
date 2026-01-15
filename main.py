"""
Port Detector Pro - 端口检测可视化工具
主程序入口
"""

import sys
import os

# 确保 src 目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
