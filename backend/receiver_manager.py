#!/usr/bin/env python3
"""
Tech-Interactives - Receiver Manager
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ReceiverManager:
    """Manage ESP32 receiver lifecycle"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.receivers: Dict[int, Dict] = {}
        self.init_receivers()
    
    def init_receivers(self):
        """Load receiver configurations"""
        for rx_config in self.config.get('receivers', []):
            rx_id = rx_config.get('id', 1)
            self.receivers[rx_id] = rx_config
    
    def get_all_receivers(self) -> Dict:
        """Get all receivers"""
        return self.receivers
    
    def get_receiver_status(self, rx_id: int) -> Dict:
        """Get receiver status"""
        return self.receivers.get(rx_id, {})
