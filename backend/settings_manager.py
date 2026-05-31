#!/usr/bin/env python3
"""
Tech-Interactives - Settings Manager
"""

import json
from pathlib import Path
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SettingsManager:
    """Manage system settings"""
    
    DEFAULT_CONFIG = {
        'system': {
            'name': 'Tech-Interactives Radar',
            'version': '1.0.0',
            'debug_mode': False
        },
        'receivers': [
            {'id': 1, 'ip': '192.168.1.101', 'port': 5002, 'position': {'x': -5, 'y': 0, 'z': -5}},
            {'id': 2, 'ip': '192.168.1.102', 'port': 5002, 'position': {'x': 5, 'y': 0, 'z': -5}}
        ],
        'detection': {
            'presence_threshold': 0.6,
            'motion_threshold': 100
        }
    }
    
    def __init__(self, config_dir: str = 'config'):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_from_file()
    
    def load_from_file(self):
        """Load config from file"""
        filepath = self.config_dir / 'system_config.json'
        if filepath.exists():
            with open(filepath) as f:
                self.config.update(json.load(f))
    
    def save_to_file(self):
        """Save config to file"""
        filepath = self.config_dir / 'system_config.json'
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default) if isinstance(value, dict) else default
        return value
    
    def set(self, key: str, value: Any):
        """Set config value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_to_file()
    
    def get_all(self) -> Dict:
        """Get all config"""
        return self.config
