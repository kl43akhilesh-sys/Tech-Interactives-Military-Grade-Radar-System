#!/usr/bin/env python3
"""
Tech-Interactives - WebSocket Server
"""

from flask import Flask
from flask_socketio import SocketIO, emit
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class WebSocketServer:
    """WebSocket real-time updates"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.socketio = SocketIO(app, cors_allowed_origins="*")
        self.register_handlers()
    
    def register_handlers(self):
        """Register WebSocket handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info('Client connected')
            emit('response', {'status': 'Connected to Tech-Interactives'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info('Client disconnected')
    
    def broadcast_detection(self, detection: Dict):
        """Broadcast detection"""
        self.socketio.emit('detection', detection, broadcast=True)
    
    def broadcast_status(self, status: Dict):
        """Broadcast status"""
        self.socketio.emit('status', status, broadcast=True)
