#!/usr/bin/env python3
"""
Tech-Interactives - Localization Engine
"""

import logging
from typing import Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class LocalizationEngine:
    """Estimate human position from multi-receiver RSSI"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.receiver_positions = config.get('receiver_positions', {})
        self.last_position = (5.0, 5.0)
    
    def localize(self, rssi_map: Dict[int, int]) -> Dict:
        """Estimate position from RSSI map"""
        
        if len(rssi_map) < 2:
            return {
                'x': 5.0,
                'y': 5.0,
                'confidence': 0.0,
                'zone': 'center'
            }
        
        # Weighted average position based on RSSI
        total_weight = 0
        weighted_x = 0
        weighted_y = 0
        
        for rx_id, rssi in rssi_map.items():
            if str(rx_id) in self.receiver_positions:
                pos = self.receiver_positions[str(rx_id)]
                distance = self.rssi_to_distance(rssi)
                weight = 1.0 / (distance + 0.1)
                
                weighted_x += pos['x'] * weight
                weighted_y += pos['y'] * weight
                total_weight += weight
        
        if total_weight > 0:
            x = weighted_x / total_weight
            y = weighted_y / total_weight
        else:
            x, y = self.last_position
        
        self.last_position = (x, y)
        confidence = min(1.0, len(rssi_map) / 3.0)
        zone = self.classify_zone(x, y)
        
        return {
            'x': float(x),
            'y': float(y),
            'confidence': float(confidence),
            'zone': zone
        }
    
    def rssi_to_distance(self, rssi: int) -> float:
        """Convert RSSI to distance"""
        tx_power = -40
        n = 2.0
        distance = 10.0 ** ((tx_power - rssi) / (10 * n))
        return max(0.1, distance)
    
    def classify_zone(self, x: float, y: float) -> str:
        """Classify position into zones"""
        zones = {
            'nw': (0, 5, 0, 5),
            'ne': (5, 10, 0, 5),
            'sw': (0, 5, 5, 10),
            'se': (5, 10, 5, 10),
            'center': (3, 7, 3, 7)
        }
        
        for zone, (x_min, x_max, y_min, y_max) in zones.items():
            if x_min <= x < x_max and y_min <= y < y_max:
                return f'zone_{zone}'
        
        return 'zone_unknown'
