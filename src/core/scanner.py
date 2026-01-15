"""
Port scanning and statistics utilities.
"""

from __future__ import annotations

import psutil
import socket
import time
from dataclasses import dataclass
from typing import Callable, Optional

START_TIME = time.time()


@dataclass
class ConnectionInfo:
    protocol: str          # TCP / UDP / OTHER
    local_addr: str
    local_port: int
    remote_addr: str
    remote_port: int
    status: str
    pid: int
    process_name: str


class PortScanner:
    """使用 psutil 获取网络连接信息"""

    def __init__(self):
        self._process_cache: dict[int, str] = {}
        self._cache_time: float = 0.0
        self._cache_ttl: float = 5.0  # 进程名缓存 5 秒

    def _get_process_name(self, pid: int) -> str:
        if pid is None or pid == 0:
            return "System"

        now = time.time()
        if now - self._cache_time > self._cache_ttl:
            self._process_cache.clear()
            self._cache_time = now

        if pid in self._process_cache:
            return self._process_cache[pid]

        try:
            proc = psutil.Process(pid)
            name = proc.name()
            self._process_cache[pid] = name
            return name
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "N/A"

    def scan_once(self) -> list[ConnectionInfo]:
        """执行一次连接扫描"""
        results: list[ConnectionInfo] = []
        try:
            for conn in psutil.net_connections(kind="all"):
                try:
                    if conn.type == socket.SOCK_STREAM:
                        protocol = "TCP"
                    elif conn.type == socket.SOCK_DGRAM:
                        protocol = "UDP"
                    else:
                        protocol = "OTHER"

                    local_addr = conn.laddr.ip if conn.laddr else ""
                    local_port = conn.laddr.port if conn.laddr else 0
                    remote_addr = conn.raddr.ip if conn.raddr else ""
                    remote_port = conn.raddr.port if conn.raddr else 0
                    status = conn.status if conn.status else "NONE"
                    pid = conn.pid or 0
                    process_name = self._get_process_name(pid)

                    results.append(
                        ConnectionInfo(
                            protocol=protocol,
                            local_addr=local_addr,
                            local_port=local_port,
                            remote_addr=remote_addr,
                            remote_port=remote_port,
                            status=status,
                            pid=pid,
                            process_name=process_name,
                        )
                    )
                except Exception:
                    continue
        except psutil.AccessDenied:
            # 如果权限不足，返回空列表
            pass
        return results


def get_statistics(connections: list[ConnectionInfo]) -> dict:
    """统计协议和状态"""
    stats = {
        "total": len(connections),
        "tcp": 0,
        "udp": 0,
        "listen": 0,
        "established": 0,
        "status_counts": {},
    }

    for c in connections:
        if c.protocol == "TCP":
            stats["tcp"] += 1
        elif c.protocol == "UDP":
            stats["udp"] += 1

        if c.status == "LISTEN":
            stats["listen"] += 1
        elif c.status == "ESTABLISHED":
            stats["established"] += 1

        stats["status_counts"][c.status] = stats["status_counts"].get(c.status, 0) + 1

    return stats


def get_process_usage(connections: list[ConnectionInfo]) -> list[tuple[str, int]]:
    """统计进程连接数量，按数量降序"""
    counts: dict[str, int] = {}
    for c in connections:
        name = c.process_name or "N/A"
        counts[name] = counts.get(name, 0) + 1
    # 排序
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def get_self_usage() -> dict:
    """获取当前 Port Detector 进程的 CPU/内存占用与运行时长"""
    proc = psutil.Process()
    # 非阻塞 CPU 百分比（相对上次调用）
    cpu_percent = proc.cpu_percent(interval=0.0)
    mem_mb = proc.memory_info().rss / (1024 * 1024)
    uptime_sec = time.time() - START_TIME
    uptime_str = _format_duration(uptime_sec)
    return {
        "cpu_percent": cpu_percent,
        "mem_mb": mem_mb,
        "uptime": uptime_str,
    }


def _format_duration(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
