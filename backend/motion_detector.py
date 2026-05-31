#!/usr/bin/env python3
"""
Tech-Interactives - Motion Detection Module
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class MotionDetector:
    """Detect motion from signal changes"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.motion_threshold = config.get('motion_threshold', 100)
        self.last_rssi = -100
    
    def detect(self, features: Dict, rx_id: int) -> Dict:
        """Detect motion from signal variance"""
        
        rssi = features.get('rssi', -100)
        variance = features.get('variance', 0)
        
        # Motion detection
        intensity = min(100.0, (variance / self.motion_threshold) * 100)
        detected = intensity > 20
        
        self.last_rssi = rssi
        
        return {
            'detected': detected,
            'intensity': float(intensity),
            'direction': 'stationary',
            'confidence': min(1.0, intensity / 100)
        }
