import json
from pathlib import Path

DEFAULT_CONFIG = {
    "active_server": "Roblox (⚡ Live In-Game Auto-Detect)",
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
            "name": "Roblox (⚡ Live In-Game Auto-Detect)",
            "host": "auto:roblox",
            "category": "🎮 Roblox"
        },
        {
            "name": "Roblox (EU - Frankfurt Datacenter)",
            "host": "ec2.eu-central-1.amazonaws.com",
            "category": "🎮 Roblox"
        },
        {
            "name": "Roblox (EU - London Datacenter)",
            "host": "ec2.eu-west-2.amazonaws.com",
            "category": "🎮 Roblox"
        },
        {
            "name": "Roblox (US - Virginia Datacenter)",
            "host": "ec2.us-east-1.amazonaws.com",
            "category": "🎮 Roblox"
        },
        {
            "name": "Roblox (US - Oregon Datacenter)",
            "host": "ec2.us-west-2.amazonaws.com",
            "category": "🎮 Roblox"
        },
        {
            "name": "Roblox (Asia - Singapore Datacenter)",
            "host": "ec2.ap-southeast-1.amazonaws.com",
            "category": "🎮 Roblox"
        },
        {
            "name": "CS2 (🇸🇪 Stockholm / EU North)",
            "host": "sto.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇩🇪 Frankfurt / EU West)",
            "host": "fra.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇵🇱 Warsaw / Poland)",
            "host": "waw.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇦🇹 Vienna / Austria)",
            "host": "vie.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇫🇮 Helsinki / Finland)",
            "host": "hel.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇬🇧 London / UK)",
            "host": "lhr.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "CS2 (🇺🇸 Virginia / US East)",
            "host": "iad.valve.net",
            "category": "🎯 CS2 / Steam"
        },
        {
            "name": "Valorant (🇩🇪 Frankfurt 1)",
            "host": "162.249.72.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Valorant (🇵🇱 Warsaw)",
            "host": "162.249.79.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Valorant (🇸🇪 Stockholm)",
            "host": "162.249.78.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Valorant (🇬🇧 London)",
            "host": "162.249.74.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Valorant (🇫🇷 Paris)",
            "host": "162.249.75.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Valorant (🇺🇸 Virginia / US East)",
            "host": "192.207.0.1",
            "category": "🏹 Valorant / Riot"
        },
        {
            "name": "Discord Voice (🇳🇱 Rotterdam / EU)",
            "host": "rotterdam.discord.gg",
            "category": "🎙 Discord Voice"
        },
        {
            "name": "Discord Voice (🇩🇪 Frankfurt / Central EU)",
            "host": "frankfurt.discord.gg",
            "category": "🎙 Discord Voice"
        },
        {
            "name": "Discord Voice (🇺🇸 US East)",
            "host": "us-east.discord.gg",
            "category": "🎙 Discord Voice"
        },
        {
            "name": "Cloudflare DNS (1.1.1.1)",
            "host": "1.1.1.1",
            "category": "🌐 DNS / Web"
        },
        {
            "name": "Google DNS (8.8.8.8)",
            "host": "8.8.8.8",
            "category": "🌐 DNS / Web"
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
                config = DEFAULT_CONFIG.copy()
                config.update(loaded)
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()

    def save_config(self, data: dict = None):
        if data is not None:
            self.data = data
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def get_active_server_info(self) -> dict:
        active_name = self.data.get("active_server")
        for s in self.data.get("servers", []):
            if s.get("name") == active_name:
                return s
        servers = self.data.get("servers", [])
        return servers[0] if servers else {"name": "Roblox", "host": "auto:roblox"}

    def set_active_server(self, server_name: str):
        self.data["active_server"] = server_name
        self.save_config()

    def set_interval(self, interval: float):
        self.data["interval_seconds"] = interval
        self.save_config()
