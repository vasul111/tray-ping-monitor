# tray-ping-monitor

A tiny Windows system tray app that shows your live ping directly in the taskbar. Built for gaming and checking connection stability on the fly without opening consoles or task manager.

![preview](https://img.shields.io/badge/ping-24ms-10B981?style=flat-square) ![platform](https://img.shields.io/badge/windows-only-0078D6?style=flat-square)

---

### Why?
Got tired of opening speedtest or cmd `ping` in the middle of a game to figure out if Roblox, Discord, or CS2 is lagging because of my ISP or server issues. This sits quietly in the tray and changes color/numbers in real-time.

---

### Features
- **Dynamic tray icon**: Shows current ping in ms right on the icon.
  - 🟢 **Green** (< 50ms) — Clean connection
  - 🟡 **Yellow** (50–110ms) — Playable
  - 🟠 **Orange** (110–180ms) — Noticeable delay
  - 🔴 **Red** (> 180ms or packet loss) — Spikes / dropped packets
- **Game presets out of the box**:
  - Roblox (Global Matchmaking)
  - Discord (Voice/Gateway)
  - Steam / Valve (EU Servers)
  - Valorant / Riot
  - Cloudflare & Google DNS
- **Stats in tooltip & menu**: Hover to see average ping, jitter (stability), and packet loss percentage.
- **Adjustable update rate**: 0.5s / 1.0s / 1.5s / 3.0s / 5.0s.
- **Custom servers**: Add any IP or domain in `config.json`.
- **Low footprint**: ~20 MB RAM, near-zero CPU.

---

### Quick Start

#### Download standalone .exe
Grab the latest `TrayPingMonitor.exe` from [Releases](https://github.com/vasul111/tray-ping-monitor/releases) and run it. No installation or Python needed.

#### Or run from source
```bash
git clone https://github.com/vasul111/tray-ping-monitor.git
cd tray-ping-monitor
pip install -r requirements.txt
python src/main.py
```

---

### Adding Custom Servers

Edit `config.json` in the same directory:

```json
{
  "servers": [
    {
      "name": "My CS2 Server",
      "host": "128.0.0.1",
      "category": "Gaming"
    }
  ]
}
```

Right-click the tray icon -> `⚙ Open Settings` to open the file directly.

---

### Building .exe

To build a single-file executable yourself:

```bash
python build_exe.py
```
Output will be in `dist/TrayPingMonitor.exe`.

---

### Roadmap / TODO
- [ ] Mini floating graph window on left click
- [ ] Sound notification when packet loss > 10%
- [ ] Auto-start with Windows toggle

---

### License
MIT
