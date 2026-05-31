#!/usr/bin/env python3
"""
Tech-Interactives Military Grade Radar System
CSI Reader Module - Manages ESP32 Receiver Connections

Author: Akhilesh TU
Organization: Tech-Interactives
Version: 1.0.0
"""

import socket
import threading
import json
import logging
from datetime import datetime
from typing import Dict, List, Callable, Optional
from collections import deque

logger = logging.getLogger(__name__)

class ReceiverConnection:
    """Manages individual ESP32 receiver connection"""
    
    def __init__(self, rx_id: int, ip: str, port: int, callback: Callable):
        self.rx_id = rx_id
        self.ip = ip
        self.port = port
        self.callback = callback
        self.socket = None
        self.running = False
        self.connected = False
        self.packets_received = 0
        self.last_packet_time = None
        self.average_rssi = -100
        self.uptime = 0
    
    def run(self):
        """Main receiver thread"""
        self.running = True
        
        while self.running:
            try:
                self.connect()
                self.receive_loop()
            except Exception as e:
                logger.error(f"RX-{self.rx_id} error: {e}")
                self.connected = False
                threading.Event().wait(2)
    
    def connect(self):
        """Connect to receiver"""
        if self.connected:
            return
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.ip, self.port))
            self.connected = True
            logger.info(f"RX-{self.rx_id} connected at {self.ip}:{self.port}")
        except socket.error as e:
            logger.warning(f"RX-{self.rx_id} connection failed: {e}")
            self.connected = False
    
    def receive_loop(self):
        """Receive data from ESP32"""
        if not self.socket:
            return
        
        buffer = ""
        
        while self.running and self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                if not data:
                    self.connected = False
                    break
                
                buffer += data
                
                # Process complete JSON lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if line:
                        try:
                            packet = json.loads(line)
                            self.process_packet(packet)
                        except json.JSONDecodeError:
                            pass
                        
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"RX-{self.rx_id} receive error: {e}")
                self.connected = False
                break
    
    def process_packet(self, packet: Dict):
        """Process received packet"""
        packet_type = packet.get('type')
        
        if packet_type == 'csi_data':
            self.packets_received += 1
            self.last_packet_time = datetime.now()
            self.average_rssi = packet.get('rssi', -100)
            self.callback(self.rx_id, packet)
        
        elif packet_type == 'heartbeat':
            self.uptime = packet.get('uptime', 0)
            self.average_rssi = packet.get('rssi', -100)
    
    def stop(self):
        """Stop receiver"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def get_status(self) -> Dict:
        """Get receiver status"""
        return {
            'rx_id': self.rx_id,
            'ip': self.ip,
            'port': self.port,
            'connected': self.connected,
            'packets_received': self.packets_received,
            'last_packet': self.last_packet_time.isoformat() if self.last_packet_time else None,
            'rssi': int(self.average_rssi),
            'uptime': self.uptime
        }

class CSIReader:
    """Main CSI Reader - Manages all ESP32 connections"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.receivers: Dict[int, ReceiverConnection] = {}
        self.running = False
        self.callbacks = []
        self.lock = threading.Lock()
        
        self.init_receivers()
    
    def init_receivers(self):
        """Initialize receiver connections from config"""
        receiver_configs = self.config.get('receivers', [])
        
        for rx_config in receiver_configs:
            rx_id = rx_config.get('id', 1)
            ip = rx_config.get('ip', f'192.168.1.{100+rx_id}')
            port = rx_config.get('port', 5002)
            
            self.receivers[rx_id] = ReceiverConnection(
                rx_id, ip, port, self.on_csi_data
            )
            logger.info(f"Initialized receiver {rx_id} at {ip}:{port}")
    
    def start(self):
        """Start CSI reader"""
        self.running = True
        logger.info("Starting CSI Reader")
        
        for rx_id, receiver in self.receivers.items():
            thread = threading.Thread(
                target=receiver.run,
                daemon=True,
                name=f"RX-{rx_id}"
            )
            thread.start()
    
    def stop(self):
        """Stop CSI reader"""
        self.running = False
        for receiver in self.receivers.values():
            receiver.stop()
    
    def on_csi_data(self, rx_id: int, packet: Dict):
        """CSI data callback"""
        for callback in self.callbacks:
            try:
                callback(rx_id, packet)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def register_callback(self, callback: Callable):
        """Register callback for CSI data"""
        self.callbacks.append(callback)
    
    def get_all_status(self) -> Dict:
        """Get all receiver status"""
        return {
            rx_id: receiver.get_status()
            for rx_id, receiver in self.receivers.items()
        }
