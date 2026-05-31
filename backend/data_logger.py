#!/usr/bin/env python3
"""
Tech-Interactives - Data Logger
"""

import json
import csv
from pathlib import Path
import logging
from typing import Dict
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

class DataLogger:
    """Log system data"""
    
    def __init__(self, log_dir: str = 'data/logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.data_buffer = {}
    
    def log_event(self, event_type: str, data: Dict):
        """Log event"""
        if event_type not in self.data_buffer:
            self.data_buffer[event_type] = deque(maxlen=1000)
        
        data['timestamp'] = datetime.now().isoformat()
        self.data_buffer[event_type].append(data)
    
    def flush_to_csv(self, event_type: str, filename: str = None):
        """Flush buffer to CSV"""
        if event_type not in self.data_buffer or len(self.data_buffer[event_type]) == 0:
            return
        
        if filename is None:
            filename = f'{event_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        filepath = self.log_dir / filename
        data = list(self.data_buffer[event_type])
        
        if data:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Flushed {len(data)} records to {filepath}")
    
    def flush_all(self):
        """Flush all buffers"""
        for event_type in list(self.data_buffer.keys()):
            self.flush_to_csv(event_type)
