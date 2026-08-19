# tray-ping-monitor

A lightweight Windows system tray utility that displays real-time latency, jitter, and packet loss to gaming datacenters and DNS servers directly in your taskbar.

---

### Why?
Most network utilities ping generic web domains behind CDNs (`google.com`, `roblox.com`), which gives misleading latency numbers and does not reflect your actual in-game connection.

This tool monitors real gaming relays and datacenters (Valve SDR for CS2, Riot European shards for Valorant, AWS datacenters for Roblox, Discord voice regions) with automatic in-game server detection.

---

### Features

- **Live Taskbar Badge**: Real-time latency number with color status:
  - Green (< 50 ms)
  - Amber (50 - 110 ms)
  - Orange (110 - 180 ms)
  - Red (> 180 ms or packet loss)
- **3 Icon Styles**:
  - `Badge` (Dark pill border with number)
  - `Minimal Dot` (Compact color indicator circle)
  - `Number Only` (Clean borderless typography)
- **Game Server Auto-Detection**:
  - **Roblox**: Real-time sniffer for `%localappdata%\Roblox\logs` that extracts your active game server IP (`128.116.x.x`) upon joining any place.
  - **CS2 / Steam**: Process-level socket tracker that monitors active Valve SDR relays while playing Counter-Strike 2.
- **Dual-Mode Latency Engine**: Seamlessly combines ICMP echo and instant TCP socket handshakes (port 443) for firewalled game networks (e.g. Valorant / Riot).
- **Hover & Menu Statistics**: Hover over the tray icon or open the right-click menu to see current ping, rolling average, jitter (stability), and packet loss percentage.
- **Windows Autostart**: Built-in toggle to run automatically on system boot.
- **Zero Overhead**: Consumes < 15 MB RAM and near-zero CPU.

---

### Supported Presets

- **Roblox**: Live In-Game Auto-Detect, EU Frankfurt, EU London, US Virginia, US Oregon, Asia Singapore
- **CS2 / Steam**: Live Match Auto-Detect, Frankfurt SDR, Stockholm SDR, Warsaw SDR, Vienna SDR, Helsinki SDR, London SDR, US Virginia SDR
- **Valorant / Riot Games**: EU Frankfurt, EU Warsaw, Global Gateway
- **Discord**: Voice Rotterdam, Voice Frankfurt, Gateway
- **DNS**: Cloudflare (`1.1.1.1`), Google (`8.8.8.8`)

---

### Quick Start

#### Download Standalone .exe (No Python Needed)
1. Download `TrayPingMonitor.exe` from [Releases](https://github.com/vasul111/tray-ping-monitor/releases).
2. Run `TrayPingMonitor.exe`.

> Note: If Windows SmartScreen shows a prompt on first launch, click **More info** -> **Run anyway**.

#### Run from Source
```bash
git clone https://github.com/vasul111/tray-ping-monitor.git
cd tray-ping-monitor
pip install -r requirements.txt
python src/main.py
```

---

### Custom Servers

Add custom endpoints directly in `config.json`:

```json
{
  "servers": [
    {
      "name": "My Custom Server",
      "host": "128.0.0.1:443",
      "category": "Custom"
    }
  ]
}
```

---

### Building .exe

```bash
python build_exe.py
```

---

### License
MIT
