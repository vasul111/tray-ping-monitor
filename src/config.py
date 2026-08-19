import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "active_server": "Cloudflare DNS (1.1.1.1)",
    "interval_seconds": 1.5,
    "history_size": 30,
    "show_number_in_tray": True,
    "thresholds": {
        "good": 50,
        "moderate": 110,
        "bad": 180
    },
    "alerts": {
        "enabled": True,
        "loss_threshold_pct": 15,
        "high_ping_threshold_ms": 200
    },
    "servers": [
        {
            "name": "Cloudflare DNS (1.1.1.1)",
            "host": "1.1.1.1",
            "category": "DNS / Web"
        },
        {
            "name": "Google DNS (8.8.8.8)",
            "host": "8.8.8.8",
            "category": "DNS / Web"
        },
        {
            "name": "Roblox (Global / AWS)",
            "host": "roblox.com",
            "category": "Gaming"
        },
        {
            "name": "Discord (Gateway)",
            "host": "discord.gg",
            "category": "Voice / Chat"
        },
        {
            "name": "Steam / Valve (EU Server)",
            "host": "162.254.197.1",
            "category": "Gaming"
        },
        {
            "name": "Valorant / Riot (EU Central)",
            "host": "162.249.72.1",
            "category": "Gaming"
        }
    ]
}

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.data = self.load_config()

    def load_config(self) -> dict:
        if not self.config_path.exists():
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(loaded)
                return config
        except Exception as e:
            print(f"[Config] Error reading {self.config_path}: {e}. Using defaults.")
            return DEFAULT_CONFIG.copy()

    def save_config(self, data: dict = None):
        if data is not None:
            self.data = data
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[Config] Error saving {self.config_path}: {e}")

    def get_active_server_info(self) -> dict:
        active_name = self.data.get("active_server")
        for s in self.data.get("servers", []):
            if s.get("name") == active_name:
                return s
        # Fallback to first
        servers = self.data.get("servers", [])
        return servers[0] if servers else {"name": "1.1.1.1", "host": "1.1.1.1"}

    def set_active_server(self, server_name: str):
        self.data["active_server"] = server_name
        self.save_config()

    def set_interval(self, interval: float):
        self.data["interval_seconds"] = interval
        self.save_config()
