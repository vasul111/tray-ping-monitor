# 🌐 Tray Ping & Network Monitor

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
</p>

<p align="center">
  <b>A lightweight, real-time Windows System Tray utility that monitors ping, packet loss, and jitter to gaming servers and DNS endpoints.</b>
</p>

---

## ✨ Features

- 🟢 **Dynamic Tray Badge**: Live latency number and color-coded status directly inside your Windows taskbar tray icon.
  - 🟢 **Green** (`< 50 ms`): Perfect connection for competitive gaming.
  - 🟡 **Yellow** (`50 - 110 ms`): Playable / moderate latency.
  - 🟠 **Orange** (`110 - 180 ms`): High ping.
  - 🔴 **Red** (`> 180 ms` or `Loss > 15%`): Spike or packet loss alert.
- 🎮 **Pre-configured Gaming & Voice Targets**:
  - **Roblox** (Global Matchmaking & AWS GameLift)
  - **Discord** (Gateway & Voice servers)
  - **Steam / Valve** (EU Counter-Strike 2 / Dota 2 servers)
  - **Valorant / Riot Games** (EU Central)
  - **Cloudflare DNS** (`1.1.1.1`) & **Google DNS** (`8.8.8.8`)
- 📊 **Advanced Real-time Metrics**:
  - Current Latency (ms)
  - Rolling Average, Min & Max Ping
  - **Jitter** (latency consistency/stability indicator)
  - **Packet Loss** (%) calculation over a rolling window
- ⏱ **Adjustable Polling Rate**: Switch between `0.5s`, `1.0s`, `1.5s`, `3.0s`, and `5.0s` in one click.
- ⚙ **Fully Customizable**: Add your own custom server IPs/domains via `config.json`.
- 🪶 **Ultra-Lightweight**: Minimal CPU and RAM footprint (< 25 MB).

---

## 📥 Quick Start

### Option 1: Run from Source (Python)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vasul111/tray-ping-monitor.git
   cd tray-ping-monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   python src/main.py
   ```

---

### Option 2: Build Standalone `.exe` (No Python Required)

To compile into a single portable `.exe` file:

```bash
python build_exe.py
```
The finished executable will be generated in the `dist/` directory (`dist/TrayPingMonitor.exe`).

---

## 🛠 Configuration (`config.json`)

You can easily modify thresholds and add custom game servers:

```json
{
    "active_server": "Cloudflare DNS (1.1.1.1)",
    "interval_seconds": 1.5,
    "history_size": 30,
    "show_number_in_tray": true,
    "thresholds": {
        "good": 50,
        "moderate": 110,
        "bad": 180
    },
    "servers": [
        {
            "name": "My Custom Game Server",
            "host": "play.myserver.com",
            "category": "Custom"
        }
    ]
}
```

---

## 🕹 Usage

- **Hover** over the tray icon to see full metrics (Server Name, Current Ping, Avg, Jitter, Packet Loss).
- **Right-Click** the tray icon to:
  - Check live connection statistics.
  - Switch active game target / server.
  - Change the polling interval.
  - Open the configuration file.
  - Exit the application.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Developed by <a href="https://github.com/vasul111">vasul111</a> • Star ⭐ this repository if you find it helpful!
</p>
