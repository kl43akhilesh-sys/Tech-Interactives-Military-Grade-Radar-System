#!/usr/bin/env python3
"""
Tech-Interactives Military Grade Radar System
Main Backend Server

Author: Akhilesh TU
Version: 1.0.0
"""

import logging
import sys
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS

# Import all modules
from csi_reader import CSIReader
from signal_processor import SignalProcessor
from presence_detector import PresenceDetector
from motion_detector import MotionDetector
from localization_engine import LocalizationEngine
from person_counter import PersonCounter
from breathing_detector import BreathingDetector
from tracking_engine import TrackingEngine
from receiver_manager import ReceiverManager
from settings_manager import SettingsManager
from diagnostics import SystemDiagnostics
from data_logger import DataLogger
from api_server import APIServer
from websocket_server import WebSocketServer

# Configure logging
Path('logs').mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RadarSystem:
    """Main Tech-Interactives Radar System"""
    
    def __init__(self):
        logger.info("="*60)
        logger.info("Tech-Interactives Military Grade Radar System")
        logger.info("Version 1.0.0")
        logger.info("Author: Akhilesh TU")
        logger.info("="*60)
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.receiver_manager = ReceiverManager(self.settings_manager.get_all())
        self.diagnostics = SystemDiagnostics()
        self.data_logger = DataLogger()
        
        # Initialize detectors
        config = self.settings_manager.get_all()
        self.signal_processor = SignalProcessor(config.get('signal_processing', {}))
        self.presence_detector = PresenceDetector(config.get('detection', {}))
        self.motion_detector = MotionDetector(config.get('detection', {}))
        self.localization_engine = LocalizationEngine(config.get('localization', {}))
        self.person_counter = PersonCounter(config.get('detection', {}))
        self.breathing_detector = BreathingDetector(config.get('breathing', {}))
        self.tracking_engine = TrackingEngine(config.get('tracking', {}))
        
        # Initialize CSI reader
        self.csi_reader = CSIReader(config)
        self.csi_reader.register_callback(self.on_csi_data)
        
        # Flask app
        self.app = Flask(__name__, static_folder='../frontend', static_url_path='')
        self.app.config['SECRET_KEY'] = 'tech-interactives-secret'
        CORS(self.app)
        
        # Initialize API and WebSocket
        self.api_server = APIServer(self.app, self.csi_reader, 
                                    self.settings_manager, self.diagnostics)
        self.websocket_server = WebSocketServer(self.app)
        
        # Register routes
        self.register_routes()
        
        logger.info("System initialized successfully")
    
    def register_routes(self):
        """Register Flask routes"""
        
        @self.app.route('/')
        def index():
            try:
                return send_from_directory('../frontend', 'index.html')
            except:
                return '<h1>Tech-Interactives Radar System</h1><p>Backend running. Open http://localhost:5000</p>'
        
        @self.app.route('/<path:filename>')
        def serve_static(filename):
            try:
                return send_from_directory('../frontend', filename)
            except:
                return 'File not found', 404
    
    def on_csi_data(self, rx_id: int, packet: dict):
        """Process CSI data"""
        try:
            # Process signal
            features = self.signal_processor.process_csi(packet)
            
            # Run detectors
            presence = self.presence_detector.detect(features, rx_id)
            motion = self.motion_detector.detect(features, rx_id)
            breathing = self.breathing_detector.detect(features, rx_id)
            
            # Create detection event
            detection = {
                'rx_id': rx_id,
                'presence': presence,
                'motion': motion,
                'breathing': breathing,
                'rssi': packet.get('rssi')
            }
            
            # Log and broadcast
            self.data_logger.log_event('detection', detection)
            self.websocket_server.broadcast_detection(detection)
            
        except Exception as e:
            logger.error(f"Error processing CSI: {e}")
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Start system"""
        logger.info(f"Starting backend on http://{host}:{port}")
        
        # Start CSI reader
        self.csi_reader.start()
        
        # Run Flask with SocketIO
        self.websocket_server.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug,
            use_reloader=False,
            allow_unsafe_werkzeug=True
        )
    
    def shutdown(self):
        """Shutdown gracefully"""
        logger.info("Shutting down")
        self.csi_reader.stop()
        self.data_logger.flush_all()

def main():
    """Main entry point"""
    try:
        system = RadarSystem()
        system.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        system.shutdown()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
