# Tech-Interactives Military Grade Radar System

**Version:** 1.0.0  
**Author:** Akhilesh TU  
**Organization:** Tech-Interactives

## Overview

A complete WiFi CSI-based human sensing and detection system using ESP32 boards with a router.

## Quick Start (5 Minutes)

### 1. Install
```bash
git clone https://github.com/kl43akhilesh-sys/Tech-Interactives-Military-Grade-Radar-System.git
cd Tech-Interactives-Military-Grade-Radar-System
.\install.bat
```

### 2. Configure WiFi in Firmware
Edit `firmware/ESP32_RECEIVER.ino`:
```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* BACKEND_IP = "192.168.1.100";  // Your PC IP
const int RECEIVER_ID = 1;  // Change to 2, 3, etc. for additional receivers
```

### 3. Flash to ESP32 Boards
- Open Arduino IDE 2.0+
- Board: ESP32 > DOIT ESP32 DEVKIT V1
- Upload `firmware/ESP32_RECEIVER.ino` to each ESP32
- For each new receiver, change `RECEIVER_ID` in code

### 4. Start System
```bash
.\start_all.bat
```

### 5. Access Dashboard
**Browser:** http://localhost:5000

## Features

✅ Real-time presence detection  
✅ Motion analysis and tracking  
✅ Human localization  
✅ Person counting  
✅ Breathing detection  
✅ 3D visualization  
✅ Multi-receiver support (2-5+ boards)  
✅ Web dashboard  
✅ REST API  
✅ System diagnostics  

## Configuration

Edit `config/system_config.json`:

```json
{
  "receivers": [
    {"id": 1, "ip": "192.168.1.101"},
    {"id": 2, "ip": "192.168.1.102"}
  ]
}
```

## System Requirements

- Windows 11 / Linux / macOS
- Python 3.14+
- 2x ESP32-WROOM-32 boards (or more)
- WiFi 2.4GHz router
- 4GB RAM, 2GB disk space

## Hardware Setup

**No wiring required.** Just:
1. Connect ESP32s to USB power (or breadboard power)
2. Program via USB cable (Arduino IDE)
3. Both boards connect to WiFi automatically

## Adding More Receivers

1. Flash same firmware to new ESP32
2. Change `RECEIVER_ID` in firmware (1, 2, 3, etc.)
3. Add to `config/system_config.json`
4. Restart backend
5. Dashboard auto-detects new receiver

## Network Setup

**Find your PC IP:**
```bash
# Windows
ipconfig

# Linux/Mac  
ifconfig
```

Update in firmware:
```cpp
const char* BACKEND_IP = "192.168.1.100";  // Your IP here
```

## API Endpoints

- `GET /api/system/info` - System info
- `GET /api/receivers` - Receiver status
- `GET /api/diagnostics` - System health
- `GET /api/settings` - Configuration

## Troubleshooting

**ESP32 not detected?**
- Install CH340/CP2102 driver
- Try different USB cable
- Restart Arduino IDE

**No WiFi connection?**
- Check SSID and password
- Verify 2.4GHz WiFi available
- Check board is flashed correctly

**Backend not connecting?**
- Verify backend IP in firmware matches your PC
- Check firewall allows port 5002
- Ensure backend is running (`python backend/main.py`)

## Documentation

See `docs/` folder for complete guides:
- INSTALL.md - Installation
- HARDWARE_SETUP.md - Hardware guide
- API_REFERENCE.md - API documentation
- FAQ.md - Frequently asked questions

## Support

**Email:** kl.43akhilesh@gmail.com  
**GitHub Issues:** Report problems

## Future Features

- Mobile app
- Cloud integration
- Advanced AI models
- More ESP32 variants

## Credits

Created by Tech-Interactives  
Founder: Akhilesh TU
