#!/usr/bin/env python3
"""
Tech-Interactives - Presence Detection Module
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class PresenceDetector:
    """Detect human presence in area"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.threshold = config.get('presence_threshold', 0.6)
    
    def detect(self, features: Dict, rx_id: int) -> Dict:
        """Detect presence from signal features"""
        
        rssi = features.get('rssi', -100)
        quality = features.get('signal_quality', 0)
        variance = features.get('variance', 0)
        
        # Detection logic
        score = 0.0
        
        if variance > 50:
            score += 0.4 * min(1.0, variance / 200)
        
        if rssi > -75:
            score += 0.3
        
        if quality > 40:
            score += 0.3 * (quality / 100)
        
        confidence = min(1.0, score)
        detected = confidence > self.threshold
        
        return {
            'detected': detected,
            'confidence': float(confidence),
            'rssi': rssi,
            'quality': quality
        }
