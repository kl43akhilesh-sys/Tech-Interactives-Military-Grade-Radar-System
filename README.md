# Tech-Interactives Military Grade Radar System

**Created by Tech-Interactives**  
**Founder: Akhilesh TU**

## Overview

The **Tech-Interactives Military Grade Radar System** is a cutting-edge WiFi CSI-based human sensing and localization platform. It leverages Channel State Information (CSI) from WiFi signals to detect presence, track motion, count persons, estimate breathing patterns, and provide real-time 3D visualization in a tactical command center interface.

### Key Features

✅ **Presence Detection** - Detect humans in coverage area  
✅ **Motion Detection** - Real-time motion tracking and analysis  
✅ **Human Localization** - Estimate position within monitored zone  
✅ **Person Counting** - Automatic occupancy estimation  
✅ **Breathing Detection** - Non-contact vital sign monitoring  
✅ **Multi-Zone Tracking** - Track movement across defined zones  
✅ **3D Visualization** - Real-time tactical dashboard with Three.js  
✅ **Scalable Architecture** - Support for multi-receiver expansion  
✅ **Health Monitoring** - Network diagnostics and receiver status  
✅ **Calibration System** - Guided baseline signal establishment  
✅ **AI-Ready Framework** - Support for ONNX model integration  
✅ **Desktop Application** - PySide6-based local dashboard  

## System Architecture

### Current Topology
```
             WiFi Router
                  ▲
                 / \
                /   \
               /     \
              /       \
          ESP32-TX   ESP32-RX1
                      (RX2 ready)
```

### Future Topology
```
             WiFi Router
                ▲
            /   |   \
           /    |    \
       RX1     RX2    RX3
                |      |
               RX4    RX5
```

## Hardware Requirements

- **1x WiFi Router** (2.4GHz capable)
- **2x ESP32-WROOM-32** development boards
- **USB-C Cables** for programming and power
- **Breadboard and Jumper Wires** (optional, for permanent setup)

## Software Stack

- **Firmware**: Arduino/ESP-IDF (C++)
- **Backend**: Python 3.14
- **Frontend**: HTML5, CSS3, JavaScript, Three.js
- **Desktop**: PySide6
- **Visualization**: Three.js 3D Engine
- **Communication**: WebSocket, TCP, UDP, Serial

## Quick Start

### 1. Prerequisites
- Windows 11
- Python 3.14+
- Arduino IDE 2.0+
- Git

### 2. Installation
```bash
git clone https://github.com/kl43akhilesh-sys/Tech-Interactives-Military-Grade-Radar-System.git
cd Tech-Interactives-Military-Grade-Radar-System
.\install.bat
```

### 3. Hardware Setup
- Flash TX firmware to first ESP32
- Flash RX firmware to second ESP32
- Connect both to WiFi network
- See [HARDWARE_SETUP.md](docs/HARDWARE_SETUP.md) for details

### 4. Start System
```bash
.\start_all.bat
```

Dashboard opens at: `http://localhost:5000`

## Documentation

| Document | Purpose |
|----------|----------|
| [INSTALL.md](docs/INSTALL.md) | Complete installation guide |
| [HARDWARE_SETUP.md](docs/HARDWARE_SETUP.md) | Hardware assembly and wiring |
| [NETWORK_SETUP.md](docs/NETWORK_SETUP.md) | WiFi network configuration |
| [CALIBRATION_GUIDE.md](docs/CALIBRATION_GUIDE.md) | Signal baseline calibration |
| [API_REFERENCE.md](docs/API_REFERENCE.md) | Backend API documentation |
| [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Development workflow |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [UPGRADE_GUIDE.md](docs/UPGRADE_GUIDE.md) | Scaling and expansion guide |
| [FAQ.md](docs/FAQ.md) | Frequently asked questions |

## Quick Navigation

- 📖 **New to the system?** Start with [INSTALL.md](docs/INSTALL.md)
- ⚙️ **Setting up hardware?** Read [HARDWARE_SETUP.md](docs/HARDWARE_SETUP.md)
- 🔧 **Configuring network?** See [NETWORK_SETUP.md](docs/NETWORK_SETUP.md)
- 📊 **Getting started with calibration?** Check [CALIBRATION_GUIDE.md](docs/CALIBRATION_GUIDE.md)
- 🐛 **Something not working?** See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- 🚀 **Expanding the system?** Read [UPGRADE_GUIDE.md](docs/UPGRADE_GUIDE.md)
- 🤔 **Got questions?** Check [FAQ.md](docs/FAQ.md)
- 👨‍💻 **Contributing code?** See [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)
- 📡 **Using the API?** Review [API_REFERENCE.md](docs/API_REFERENCE.md)

## Repository Structure

```
Tech-Interactives-Military-Grade-Radar-System/
├── firmware/                      # ESP32 firmware
│   ├── tx/                       # Transmitter firmware
│   ├── rx/                       # Receiver firmware
│   └── shared/                   # Shared libraries
├── backend/                      # Python backend
│   ├── csi_reader.py            # CSI data acquisition
│   ├── signal_processor.py       # Signal processing
│   ├── presence_detector.py      # Presence detection
│   ├── motion_detector.py        # Motion detection
│   ├── localization_engine.py    # Position estimation
│   ├── tracking_engine.py        # Multi-object tracking
│   ├── breathing_detector.py     # Vital sign analysis
│   ├── person_counter.py         # Occupancy counting
│   ├── receiver_manager.py       # Receiver coordination
│   ├── router_manager.py         # Router communication
│   ├── network_manager.py        # Network operations
│   ├── settings_manager.py       # Configuration management
│   ├── diagnostics.py            # System diagnostics
│   ├── data_logger.py            # Data recording
│   ├── api_server.py             # REST API
│   ├── websocket_server.py       # WebSocket server
│   └── main.py                   # Entry point
├── frontend/                     # Web dashboard
│   ├── index.html               # Main dashboard
│   ├── style.css                # Styling
│   ├── app.js                   # Application logic
│   ├── dashboard.js             # Dashboard manager
│   ├── three_scene.js           # 3D visualization
│   ├── websocket_client.js      # Real-time updates
│   ├── settings_panel.js        # Settings interface
│   ├── zone_map.js              # Zone mapping
│   └── human_tracker.js         # Tracking visualization
├── desktop/                      # PySide6 desktop application
│   ├── main_window.py           # Main window
│   ├── dashboard_widget.py      # Dashboard widget
│   ├── settings_widget.py       # Settings widget
│   └── run.py                   # Desktop app entry
├── models/                       # AI models directory
│   ├── presence_model.onnx      # Presence detection model
│   ├── motion_model.onnx        # Motion detection model
│   ├── localization_model.onnx  # Localization model
│   └── tracking_model.onnx      # Tracking model
├── assets/                       # 3D models and media
│   ├── models/
│   ├── icons/
│   ├── sounds/
│   └── fonts/
├── config/                       # Configuration files
│   ├── system_config.json       # System configuration
│   ├── receiver_config.json     # Receiver settings
│   ├── network_config.json      # Network settings
│   └── ai_config.json           # AI model settings
├── docs/                         # Documentation
├── scripts/                      # Installation and utility scripts
├── tests/                        # Unit and integration tests
├── requirements.txt              # Python dependencies
├── install.bat                   # Windows installer
├── setup.ps1                     # PowerShell setup
├── start_all.bat                 # System startup
└── .gitignore                    # Git ignore rules
```

## System Data Flow

```
WiFi Router (CSI Source)
        ↓
ESP32-TX (Transmits packets)
        ↓
ESP32-RX1/RX2 (Capture CSI)
        ↓
Python Backend (Central Intelligence)
        ├── CSI Reader (Data acquisition)
        ├── Signal Processor (Filtering & Feature extraction)
        ├── Motion Detector (Movement analysis)
        ├── Presence Detector (Human presence)
        ├── Localization Engine (Position estimation)
        ├── Breathing Detector (Vital signs)
        ├── Tracking Engine (Multi-object tracking)
        └── Person Counter (Occupancy estimation)
        ↓
WebSocket Server (Real-time distribution)
        ↓
┌───────┴──────────────┬──────────────┐
│                      │              │
Web Dashboard    Desktop App    REST API
(Three.js 3D)    (PySide6)    (JSON)
```

## Key Capabilities

### Presence Detection
- Real-time human presence detection
- Confidence scoring
- Multi-zone support
- Configurable sensitivity

### Motion Analysis
- Movement detection and intensity
- Motion direction estimation
- Speed calculation
- Motion trails visualization

### Localization
- WiFi fingerprinting
- Signal triangulation
- Position estimation in 2D space
- Zone-based classification

### Person Counting
- Automatic occupancy estimation
- Multi-person tracking
- Person entry/exit detection
- Crowd density estimation

### Breathing Detection
- Non-contact vital sign monitoring
- Breathing rate extraction
- Heart rate motion estimation
- Signal quality assessment

### Network Diagnostics
- Receiver health monitoring
- Packet loss detection
- Signal quality metrics
- Network latency tracking
- CSI sample rate monitoring

## Configuration

All system settings are managed through:
1. **Web Settings Panel** - Browser-based configuration
2. **Configuration Files** - JSON-based settings
3. **Environment Variables** - System-level configuration
4. **Calibration Wizard** - Guided setup process

## Scalability

The system is designed to scale from 2 receivers to 5+ receivers:

- **Phase 1**: TX + RX1 (Current)
- **Phase 2**: TX + RX1 + RX2 (Dual receiver)
- **Phase 3**: TX + RX1 + RX2 + RX3 (Triangle configuration)
- **Phase 4**: TX + RX1-RX5 (Multi-receiver array)

No code changes required—only configuration updates.

## AI Integration

The system supports ONNX model integration for:
- Presence detection
- Motion classification
- Localization refinement
- Breathing pattern analysis
- Advanced tracking

Custom models can be trained and deployed without code modification.

## Performance Specifications

| Metric | Value |
|--------|-------|
| CSI Sample Rate | 100+ Hz |
| Detection Latency | <500ms |
| Localization Accuracy | ±1-2m |
| Person Counting | ±1 person |
| Breathing Detection | 8-20 breaths/min |
| Maximum Range | ~20m (in-room) |
| Processing CPU | <30% on modern hardware |
| Memory Usage | <500MB |

## Version

**v1.0.0** - Initial Release
- Core WiFi CSI sensing
- Real-time 3D visualization
- Multi-zone detection
- Breathing analysis
- AI-ready architecture
- Desktop application
- Comprehensive documentation

---

**Tech-Interactives**: Building the future of WiFi sensing.  
**Created by Akhilesh TU**

For detailed setup and usage, see the documentation in the `docs/` folder.
