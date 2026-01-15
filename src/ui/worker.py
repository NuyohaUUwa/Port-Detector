"""
Worker thread for running port scans in background
"""

from PyQt6.QtCore import QThread, pyqtSignal
from src.core.scanner import PortScanner, ConnectionInfo

class ScanWorker(QThread):
    """Background worker for port scanning"""
    
    # Signals
    data_ready = pyqtSignal(list)  # Emits list[ConnectionInfo]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanner = PortScanner()
        self.is_running = False
        self.interval = 2.0
    
    def run(self):
        """Thread main loop"""
        self.is_running = True
        
        # Use the scanner's existing logic but control the loop here
        # so we can emit Qt signals
        while self.is_running:
            import time
            start = time.time()
            
            # Perform scan
            connections = self.scanner.scan_once()
            self.data_ready.emit(connections)
            
            # Calculate wait time
            elapsed = time.time() - start
            wait_time = max(0.1, self.interval - elapsed)
            
            # Sleep in small chunks to check for stop request
            waited = 0
            step = 0.1
            while waited < wait_time and self.is_running:
                time.sleep(min(step, wait_time - waited))
                waited += step
    
    def stop(self):
        """Stop the scanning loop"""
        self.is_running = False
        self.wait()
        
    def set_interval(self, interval: float):
        """Set scan interval in seconds"""
        self.interval = interval
    
    def force_scan(self):
        """Trigger an immediate scan (if running)"""
        # Logic is handled in the loop, but we could interrupt the sleep.
        # For simplicity, we just let the next loop handle it or 
        # the user waits for the next interval.
        pass
