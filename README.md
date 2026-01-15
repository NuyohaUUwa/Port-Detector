# ⚡ Port Detector Pro

一款基于 **PyQt6** 的 Windows 端口检测可视化工具，实时监控系统端口使用情况。

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能特性

- **实时监控**：后台线程持续扫描，自动刷新连接列表
- **进程关联**：显示端口对应的进程名与 PID
- **可视化统计**：甜甜圈图展示 TCP/UDP 分布
- **智能搜索/筛选**：按端口、IP、进程名过滤，协议快速切换
- **localhost 专视图**：独立页面仅展示本机环回地址连接
- **查询空白端口**：一键获取 5 个当前未被占用的 localhost 端口
- **深色主题**：一致的深色 UI 风格

## 🚀 快速开始

```bash
# 1) 安装依赖
pip install -r requirements.txt

# 2) 运行
python main.py
```

> ⚠️ 建议以管理员权限运行以获取完整端口信息。

### 打包为 EXE

```bash
build.bat
```

打包后生成 `dist/PortDetector.exe`，可直接分发。

## 📦 依赖

| 库 | 版本 | 用途 |
| --- | --- | --- |
| PyQt6 | 最新 | 桌面 UI 框架 |
| psutil | 5.9.8 | 系统端口/进程信息 |

## 📁 项目结构

```
Port Detector/
├── main.py
├── requirements.txt
├── build.bat
└── src/
    ├── core/
    │   ├── scanner.py      # 端口扫描核心
    │   └── ports.py        # 查询空白端口工具
    └── ui/
        ├── styles.py       # 主题样式 (QSS)
        ├── worker.py       # 扫描线程适配
        ├── main_window.py  # 主窗口
        ├── widgets/
        │   ├── sidebar.py       # 侧边栏
        │   └── donut_chart.py   # 协议分布图
        └── views/
            ├── dashboard.py      # 仪表盘
            ├── port_table.py     # 全量端口表
            └── localhost_ports.py # localhost 专视图
```

## 🎨 主题

深色主题（与应用一致），包含卡片、按钮、表格的统一配色与 QSS。

## 📄 许可证

MIT License
