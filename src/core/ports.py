"""
Utility for finding currently free localhost TCP ports.
"""

import socket
from typing import List


def get_free_ports(count: int = 5, min_port: int = 1024, max_port: int = 65535) -> List[int]:
    """
    Return a list of free localhost ports.
    Ports are obtained by binding to port 0 (OS assigns), then immediately closing.
    """
    ports: List[int] = []
    sockets = []

    try:
        for _ in range(count):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("localhost", 0))
            s.listen(1)
            port = s.getsockname()[1]
            if min_port <= port <= max_port:
                ports.append(port)
                sockets.append(s)
            else:
                s.close()
        return ports
    finally:
        for s in sockets:
            try:
                s.close()
            except OSError:
                pass
