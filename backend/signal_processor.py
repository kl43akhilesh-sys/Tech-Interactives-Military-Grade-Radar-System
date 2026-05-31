#!/usr/bin/env python3
"""
Tech-Interactives - Signal Processing Module
"""

import numpy as np
from scipy import signal as scipy_signal
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SignalProcessor:
    """Process CSI signals and extract features"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.window_size = config.get('window_size', 100)
    
    def process_csi(self, packet: Dict) -> Dict:
        """Process CSI packet and extract features"""
        
        features = {
            'timestamp': packet.get('timestamp'),
            'rssi': packet.get('rssi', -100),
            'rate': packet.get('rate'),
            'mcs': packet.get('mcs'),
            'csi_len': packet.get('csi_len')
        }
        
        # Calculate signal metrics
        rssi = packet.get('rssi', -100)
        features['signal_quality'] = self.calculate_signal_quality(rssi)
        features['variance'] = self.estimate_variance(rssi)
        features['entropy'] = self.calculate_entropy(rssi)
        
        return features
    
    def calculate_signal_quality(self, rssi: int) -> float:
        """Convert RSSI to quality 0-100%"""
        # RSSI range: -100 (worst) to -30 (best)
        quality = max(0, min(100, (rssi + 100) * 2))
        return quality
    
    def estimate_variance(self, rssi: int) -> float:
        """Estimate signal variance (for motion detection)"""
        # Higher RSSI variation = more motion
        # Simplified: use noise floor estimation
        noise_floor = 95  # dBm (typical WiFi noise floor)
        variance = abs(rssi - noise_floor) * 2
        return variance
    
    def calculate_entropy(self, rssi: int) -> float:
        """Calculate signal entropy"""
        # Entropy increases with multi-path
        quality = self.calculate_signal_quality(rssi)
        entropy = -quality * np.log2(quality + 0.001)
        return entropy
