# tray-ping-monitor

Lightweight Windows system tray application that monitors live ping, jitter, and packet loss to game datacenters and DNS endpoints.

---

### Key Capabilities

- **Roblox**:
  - Live In-Game Auto-Detect (reads active server IP directly from client logs)
  - Regional datacenters: EU Frankfurt, EU London, US Virginia, US Oregon, Asia Singapore
- **CS2 / Steam**:
  - Valve SDR Relays: Stockholm, Frankfurt, Warsaw, Vienna, Helsinki, London, Virginia
- **Valorant / Riot Games**:
  - Low-latency endpoints: Frankfurt, Warsaw, Global
- **Discord Voice**:
  - Regional servers: Rotterdam, Frankfurt, Gateway
- **DNS / Internet Baseline**:
  - Cloudflare (1.1.1.1) and Google (8.8.8.8)

---

### Tray Features

- **Anti-aliased Tray Badge**: Displays real-time latency with clean color status:
  - Green (< 50 ms)
  - Amber (50 - 110 ms)
  - Orange (110 - 180 ms)
  - Red (> 180 ms or packet loss)
- **Categorized Menu**: Clean right-click context menu grouped by game and service.
- **Metrics on Hover**: Current ping, rolling average, jitter (stability), and packet loss percentage.
- **Dual-Mode Latency Engine**: Automatic ICMP echo with seamless TCP socket fallback for firewalled game servers (e.g. Riot/Valorant).

---

### Quick Start

#### Option 1: Standalone .exe (No Python Required)
1. Download `TrayPingMonitor.exe` from [Releases](https://github.com/vasul111/tray-ping-monitor/releases).
2. Run `TrayPingMonitor.exe`.

> Note: If Windows SmartScreen shows a warning on first launch, click **More info** -> **Run anyway**. This is standard for newly published unsigned open-source binaries.

#### Option 2: Run from Source
```bash
git clone https://github.com/vasul111/tray-ping-monitor.git
cd tray-ping-monitor
pip install -r requirements.txt
python src/main.py
```

---

### Custom Configuration

Edit `config.json` to add custom endpoints:

```json
{
  "servers": [
    {
      "name": "Custom Server",
      "host": "1.2.3.4:443",
      "category": "Custom"
    }
  ]
}
```

---

### Building Executable

```bash
python build_exe.py
```

---

### License
MIT
