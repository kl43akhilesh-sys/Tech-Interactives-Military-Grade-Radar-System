#!/usr/bin/env python3
"""
Tech-Interactives - API Server
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

logger = logging.getLogger(__name__)

class APIServer:
    """REST API Server"""
    
    def __init__(self, app: Flask, csi_reader, settings_manager, diagnostics):
        self.app = app
        self.csi_reader = csi_reader
        self.settings_manager = settings_manager
        self.diagnostics = diagnostics
        
        CORS(self.app)
        self.register_routes()
    
    def register_routes(self):
        """Register API routes"""
        
        @self.app.route('/api/system/info', methods=['GET'])
        def get_system_info():
            return jsonify({
                'name': 'Tech-Interactives Radar',
                'version': '1.0.0',
                'author': 'Akhilesh TU'
            })
        
        @self.app.route('/api/receivers', methods=['GET'])
        def get_receivers():
            return jsonify(self.csi_reader.get_all_status())
        
        @self.app.route('/api/diagnostics', methods=['GET'])
        def get_diagnostics():
            return jsonify(self.diagnostics.get_full_diagnostics())
        
        @self.app.route('/api/settings', methods=['GET'])
        def get_settings():
            return jsonify(self.settings_manager.get_all())
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            receivers = self.csi_reader.get_all_status()
            connected = sum(1 for r in receivers.values() if r['connected'])
            return jsonify({
                'status': 'healthy',
                'connected_receivers': connected,
                'total_receivers': len(receivers)
            })
