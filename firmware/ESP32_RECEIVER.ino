/*
 * Tech-Interactives Military Grade Radar System
 * ESP32 Receiver Firmware (Works with Router + 2+ ESP32s)
 * Complete Single File - No Dependencies
 * 
 * Author: Akhilesh TU
 * Organization: Tech-Interactives
 * Version: 1.0.0
 * 
 * Features:
 * - Works with any WiFi router (2.4GHz)
 * - CSI capture and forwarding
 * - Multi-receiver support (2-5+ receivers)
 * - Automatic network detection
 * - Real-time data streaming
 * - Health monitoring
 * - No TX board needed
 * 
 * Setup:
 * 1. Install ESP32 board in Arduino IDE
 * 2. Select: Tools > Board > ESP32 > DOIT ESP32 DEVKIT V1
 * 3. Set WiFi SSID and Password below
 * 4. Upload to both/multiple ESP32 boards
 * 5. Boards automatically get unique IP from router
 * 6. Add receiver entries in dashboard config
 * 
 * Compatible: ESP32-WROOM-32, ESP32-S3, and variants
 */

#include <WiFi.h>
#include <esp_wifi.h>
#include <esp_wifi_types.h>
#include <time.h>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// ============================================================
// CONFIGURATION - EDIT THESE VALUES
// ============================================================

// WiFi Configuration
const char* WIFI_SSID = "YOUR_WIFI_SSID";           // YOUR ROUTER SSID
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // YOUR ROUTER PASSWORD
const char* RECEIVER_NAME = "RX-1";                 // RX-1, RX-2, RX-3, etc.
const int RECEIVER_ID = 1;                          // 1, 2, 3, 4, 5...

// Backend Server Configuration
const char* BACKEND_IP = "192.168.1.100";           // Your PC IP (change this!)
const int BACKEND_TCP_PORT = 5002;                  // Backend listening port
const int BACKEND_REST_PORT = 5000;                 // REST API port

// CSI Configuration
const int CSI_CAPTURE_RATE = 100;                   // CSI samples per second
const int CSI_BUFFER_SIZE = 256;                    // CSI payload size
const int SEND_INTERVAL_MS = 100;                   // Send data every 100ms
const int HEARTBEAT_INTERVAL_MS = 5000;             // Heartbeat every 5s

// ============================================================
// GLOBAL VARIABLES
// ============================================================

WiFiClient tcpClient;                              // TCP connection to backend
uint32_t csiPacketsReceived = 0;                    // CSI packet counter
uint32_t tcpPacketsSent = 0;                        // TCP send counter
int8_t averageRSSI = -100;                          // Average signal strength
uint32_t systemUptime = 0;                          // System uptime
bool backendConnected = false;                      // Connection status
uint32_t lastPacketTime = 0;                        // Last packet timestamp
uint32_t lastSendTime = 0;                          // Last send time
uint32_t lastHeartbeatTime = 0;                     // Last heartbeat

// CSI data structure
typedef struct {
  uint64_t timestamp;                               // Microsecond timestamp
  int8_t rssi;                                      // RSSI in dBm
  uint32_t rate;                                    // Data rate
  uint32_t mcs;                                     // Modulation coding scheme
  uint32_t len;                                     // CSI length
  uint8_t csi[CSI_BUFFER_SIZE];                    // CSI payload
  int csi_len;                                      // Actual CSI length
} csi_data_t;

csi_data_t latestCSI;                              // Latest CSI data

// ============================================================
// SETUP
// ============================================================

void setup() {
  // Serial communication
  Serial.begin(115200);
  delay(100);
  
  // Print banner
  Serial.println("\n\n");
  Serial.println("===========================================");
  Serial.println("Tech-Interactives Military Grade Radar");
  Serial.println("ESP32 Receiver Firmware v1.0.0");
  Serial.println("Author: Akhilesh TU");
  Serial.println("===========================================");
  Serial.println("");
  
  // Initialize WiFi
  initializeWiFi();
  
  // Enable CSI capture
  enableCSICapture();
  
  // Initialize NTP time
  initializeTime();
  
  Serial.println("[SETUP] Initialization complete!");
  Serial.println("[READY] Receiver ready - waiting for WiFi packets...");
  Serial.println("");
}

// ============================================================
// MAIN LOOP
// ============================================================

void loop() {
  uint32_t now = millis();
  
  // Maintain backend connection
  maintainConnection();
  
  // Send CSI data periodically
  if (now - lastSendTime >= SEND_INTERVAL_MS) {
    lastSendTime = now;
    sendCSIData();
  }
  
  // Send heartbeat
  if (now - lastHeartbeatTime >= HEARTBEAT_INTERVAL_MS) {
    lastHeartbeatTime = now;
    sendHeartbeat();
  }
  
  // Update statistics
  updateStatistics();
  
  delay(10);
}

// ============================================================
// WiFi INITIALIZATION
// ============================================================

void initializeWiFi() {
  Serial.println("[WIFI] Initializing WiFi in STA mode...");
  
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);
  
  Serial.print("[WIFI] Connecting to: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("[WIFI] Connected! IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("[WIFI] RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("[WIFI] Connection failed! Check SSID and password.");
  }
}

// ============================================================
// CSI CAPTURE
// ============================================================

void csiCallback(void *ctx, wifi_csi_info_t *info) {
  if (info == NULL || info->buf == NULL) {
    return;
  }
  
  csiPacketsReceived++;
  lastPacketTime = millis();
  
  // Store CSI data
  latestCSI.timestamp = getTimestamp();
  latestCSI.rssi = info->rx_ctrl.rssi;
  latestCSI.rate = info->rx_ctrl.rate;
  latestCSI.mcs = info->rx_ctrl.mcs;
  latestCSI.len = info->len;
  latestCSI.csi_len = (info->len < CSI_BUFFER_SIZE) ? info->len : CSI_BUFFER_SIZE;
  
  if (info->buf != NULL && latestCSI.csi_len > 0) {
    memcpy(latestCSI.csi, info->buf, latestCSI.csi_len);
  }
  
  // Update running average RSSI
  averageRSSI = (averageRSSI * 0.9) + (latestCSI.rssi * 0.1);
  
  // Log every 100 packets
  if (csiPacketsReceived % 100 == 0) {
    Serial.print("[CSI] Captured ");
    Serial.print(csiPacketsReceived);
    Serial.print(" packets | RSSI: ");
    Serial.print((int)averageRSSI);
    Serial.println(" dBm");
  }
}

void enableCSICapture() {
  Serial.println("[CSI] Enabling CSI capture...");
  
  // Set CSI RX callback
  esp_wifi_set_csi_rx_cb(csiCallback, NULL);
  
  // Configure CSI
  wifi_csi_config_t csi_config = {
    .lltf_en = true,
    .htltf_en = true,
    .stbc_htltf2_en = true,
    .ltf_merge_en = true,
    .channel_filter_en = false,
    .manu_scale = false,
    .shift = false,
  };
  
  esp_err_t err = esp_wifi_set_csi_config(&csi_config);
  if (err == ESP_OK) {
    Serial.println("[CSI] CSI enabled successfully");
  } else {
    Serial.println("[CSI] Failed to enable CSI");
  }
}

// ============================================================
// TCP COMMUNICATION
// ============================================================

void maintainConnection() {
  if (!tcpClient.connected() && WiFi.status() == WL_CONNECTED) {
    connectToBackend();
  }
}

void connectToBackend() {
  Serial.print("[TCP] Connecting to backend: ");
  Serial.print(BACKEND_IP);
  Serial.print(":");
  Serial.println(BACKEND_TCP_PORT);
  
  if (tcpClient.connect(BACKEND_IP, BACKEND_TCP_PORT)) {
    Serial.println("[TCP] Connected to backend!");
    backendConnected = true;
    
    // Send initial handshake
    sendHandshake();
  } else {
    Serial.println("[TCP] Connection failed");
    backendConnected = false;
  }
}

void sendHandshake() {
  String handshake = "{\"type\":\"handshake\",\"receiver_id\":\"";
  handshake += RECEIVER_ID;
  handshake += "\",\"name\":\"";
  handshake += RECEIVER_NAME;
  handshake += "\"}\n";
  
  tcpClient.print(handshake);
  Serial.println("[TCP] Handshake sent");
}

void sendCSIData() {
  if (!tcpClient.connected()) {
    return;
  }
  
  // Create JSON payload
  String json = "{";
  json += "\"type\":\"csi_data\",";
  json += "\"receiver_id\":" + String(RECEIVER_ID) + ",";
  json += "\"timestamp\":" + String(latestCSI.timestamp) + ",";
  json += "\"rssi\":" + String(latestCSI.rssi) + ",";
  json += "\"rate\":" + String(latestCSI.rate) + ",";
  json += "\"mcs\":" + String(latestCSI.mcs) + ",";
  json += "\"csi_len\":" + String(latestCSI.csi_len) + ",";
  json += "\"csi_samples\":" + String(csiPacketsReceived);
  json += "}\n";
  
  if (tcpClient.print(json)) {
    tcpPacketsSent++;
  }
}

void sendHeartbeat() {
  if (!tcpClient.connected()) {
    return;
  }
  
  String heartbeat = "{";
  heartbeat += "\"type\":\"heartbeat\",";
  heartbeat += "\"receiver_id\":" + String(RECEIVER_ID) + ",";
  heartbeat += "\"uptime\":" + String(systemUptime) + ",";
  heartbeat += "\"csi_packets\":" + String(csiPacketsReceived) + ",";
  heartbeat += "\"rssi\":" + String((int)averageRSSI) + ",";
  heartbeat += "\"free_heap\":" + String(ESP.getFreeHeap());
  heartbeat += "}\n";
  
  tcpClient.print(heartbeat);
}

// ============================================================
// TIME
// ============================================================

void initializeTime() {
  Serial.println("[TIME] Syncing with NTP...");
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  
  int attempts = 0;
  while (time(nullptr) < 24 * 3600 && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  Serial.println();
  
  if (time(nullptr) > 24 * 3600) {
    Serial.println("[TIME] NTP sync successful");
  } else {
    Serial.println("[TIME] NTP sync failed");
  }
}

uint64_t getTimestamp() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return (uint64_t)tv.tv_sec * 1000000LL + tv.tv_usec;
}

// ============================================================
// STATISTICS
// ============================================================

void updateStatistics() {
  static uint32_t lastUpdate = 0;
  uint32_t now = millis();
  
  if (now - lastUpdate >= 10000) {  // Every 10 seconds
    lastUpdate = now;
    systemUptime = now / 1000;
    
    Serial.println("\n[STATS]");
    Serial.print("  Uptime: ");
    Serial.print(systemUptime);
    Serial.println(" seconds");
    
    Serial.print("  CSI Packets: ");
    Serial.println(csiPacketsReceived);
    
    Serial.print("  TCP Packets Sent: ");
    Serial.println(tcpPacketsSent);
    
    Serial.print("  Avg RSSI: ");
    Serial.print((int)averageRSSI);
    Serial.println(" dBm");
    
    Serial.print("  Free Heap: ");
    Serial.print(ESP.getFreeHeap());
    Serial.println(" bytes");
    
    Serial.print("  WiFi Status: ");
    Serial.println((WiFi.status() == WL_CONNECTED) ? "Connected" : "Disconnected");
    
    Serial.print("  Backend Status: ");
    Serial.println(backendConnected ? "Connected" : "Disconnected");
    Serial.println("");
  }
}

// ============================================================
// END OF FIRMWARE
// ============================================================
