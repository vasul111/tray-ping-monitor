# tray-ping-monitor

A lightweight Windows system tray app that monitors live ping, jitter, and packet loss to actual game datacenters and DNS endpoints.

![preview](https://img.shields.io/badge/ping-24ms-10B981?style=flat-square) ![platform](https://img.shields.io/badge/windows-only-0078D6?style=flat-square)

---

### Why?
Most ping tools only ping generic web domains (like `google.com` or `roblox.com` behind CDNs), which doesn't reflect your actual in-game connection. 

This tool monitors real regional game datacenters (Valve SDR relays for CS2, Riot shards for Valorant, AWS/Roblox game servers, Discord voice regions) and can even **auto-detect the exact Roblox game server IP** you are currently connected to in real-time.

---

### Supported Game Servers & Presets

- 🎮 **Roblox**:
  - **⚡ Live In-Game Auto-Detect** (automatically reads active game server IP from client logs)
  - EU (Frankfurt / London)
  - US East (Virginia) / US West (Oregon)
  - Asia (Singapore)
- 🎯 **Counter-Strike 2 / Steam (Valve SDR Relays)**:
  - Stockholm (EU North)
  - Frankfurt (EU West)
  - Warsaw (Poland)
  - Vienna (Austria)
  - Helsinki (Finland)
  - London (UK)
  - Virginia (US East)
- 🏹 **Valorant / Riot Games**:
  - Frankfurt 1 / Warsaw / Stockholm / London / Paris / Virginia
- 🎙 **Discord Voice**:
  - Rotterdam / Frankfurt / US East
- 🌐 **DNS / Core**:
  - Cloudflare (`1.1.1.1`) & Google (`8.8.8.8`)

---

### Features
- **Dynamic tray icon**: Displays latency number in ms directly in taskbar tray.
  - 🟢 **Green** (< 50ms) — Low ping
  - 🟡 **Yellow** (50–110ms) — Moderate
  - 🟠 **Orange** (110–180ms) — High latency
  - 🔴 **Red** (> 180ms or packet loss) — Lag spike / packet drop
- **Categorized context menu**: Switch games and regions in 1 click.
- **Detailed stats on hover**: Average ping, jitter (stability), and packet loss percentage.
- **Customizable rate**: 0.5s / 1.0s / 1.5s / 3.0s polling.
- **Custom servers**: Add your own IP/domain in `config.json`.

---

### Quick Start

#### Download standalone .exe
Download the latest `TrayPingMonitor.exe` from [Releases](https://github.com/vasul111/tray-ping-monitor/releases) and launch it.

#### Or run from source
```bash
git clone https://github.com/vasul111/tray-ping-monitor.git
cd tray-ping-monitor
pip install -r requirements.txt
python src/main.py
```

---

### License
MIT
