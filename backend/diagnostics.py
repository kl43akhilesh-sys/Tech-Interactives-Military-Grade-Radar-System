#!/usr/bin/env python3
"""
Tech-Interactives - Diagnostics Module
"""

import psutil
import platform
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)

class SystemDiagnostics:
    """System health and diagnostics"""
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_system_info(self) -> Dict:
        """Get system info"""
        return {
            'os': platform.system(),
            'platform': platform.platform(),
            'python_version': platform.python_version()
        }
    
    def get_cpu_info(self) -> Dict:
        """Get CPU info"""
        return {
            'usage_percent': psutil.cpu_percent(interval=0.1),
            'count': psutil.cpu_count()
        }
    
    def get_memory_info(self) -> Dict:
        """Get memory info"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent
        }
    
    def get_uptime(self) -> int:
        """Get uptime in seconds"""
        return int((datetime.now() - self.start_time).total_seconds())
    
    def get_full_diagnostics(self) -> Dict:
        """Get complete diagnostics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': self.get_uptime(),
            'system': self.get_system_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info()
        }
