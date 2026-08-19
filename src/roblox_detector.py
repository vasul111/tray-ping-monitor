import os
import re
from pathlib import Path

class RobloxServerDetector:
    def __init__(self):
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        self.logs_dir = Path(local_app_data) / "Roblox" / "logs" if local_app_data else None
        self.ip_pattern = re.compile(r"Connection accepted from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

    def get_latest_server_ip(self) -> tuple[str | None, str]:
        if not self.logs_dir or not self.logs_dir.exists():
            return None, "Roblox logs directory not found"

        try:
            log_files = list(self.logs_dir.glob("*_Player_*.log"))
            if not log_files:
                return None, "No Roblox player logs found"

            latest_log = max(log_files, key=lambda p: p.stat().st_mtime)

            # Read log file efficiently
            with open(latest_log, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            matches = self.ip_pattern.findall(content)
            if matches:
                latest_ip = matches[-1]
                return latest_ip, f"Roblox Live: {latest_ip}"

            return None, "Roblox: Not In-Game"
        except Exception as e:
            return None, f"Error: {e}"
