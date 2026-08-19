import os
import sys
import subprocess
from pathlib import Path
import pystray
from pystray import MenuItem as item, Menu

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import ConfigManager
from src.pinger import BackgroundPinger
from src.icon_drawer import IconDrawer

class TrayPingApp:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).parent
        else:
            self.base_dir = Path(__file__).resolve().parent.parent

        self.config_manager = ConfigManager(str(self.base_dir / "config.json"))
        self.config = self.config_manager.data
        self.drawer = IconDrawer(self.config.get("thresholds"))
        
        active_server = self.config_manager.get_active_server_info()
        self.pinger = BackgroundPinger(
            host=active_server.get("host", "roblox.com"),
            interval=self.config.get("interval_seconds", 1.5),
            history_size=self.config.get("history_size", 30),
            on_update_callback=self.on_ping_update
        )

        self.icon = None
        self.last_snap = None

    def on_ping_update(self, snap: dict):
        self.last_snap = snap
        if not self.icon:
            return

        ping = snap.get("current")
        loss = snap.get("loss", 0.0)
        show_num = self.config.get("show_number_in_tray", True)
        
        img = self.drawer.create_tray_icon(ping, loss, show_number=show_num)
        self.icon.icon = img

        active_name = self.config.get("active_server", "Target")
        if ping is not None:
            self.icon.title = f"⚡ {active_name}\nPing: {ping} ms | Loss: {loss}%\nAvg: {snap.get('avg', 0)} ms | Jitter: {snap.get('jitter', 0)} ms"
        else:
            self.icon.title = f"⚠️ {active_name}\nStatus: Timeout | Loss: {loss}%"

    def select_server(self, server_name: str):
        def handler(icon, item):
            self.config_manager.set_active_server(server_name)
            server_info = self.config_manager.get_active_server_info()
            self.pinger.set_target(server_info.get("host", "roblox.com"))
            self.update_menu()
        return handler

    def select_interval(self, interval_sec: float):
        def handler(icon, item):
            self.config_manager.set_interval(interval_sec)
            self.pinger.set_interval(interval_sec)
            self.update_menu()
        return handler

    def open_config_file(self, icon, item):
        config_path = self.base_dir / "config.json"
        if sys.platform == "win32":
            os.startfile(str(config_path))
        else:
            subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", str(config_path)])

    def exit_app(self, icon, item):
        self.pinger.stop()
        if self.icon:
            self.icon.stop()

    def _get_server_items(self):
        active_server = self.config.get("active_server")
        items = []
        for s in self.config.get("servers", []):
            name = s.get("name", "Unknown")
            items.append(item(
                name,
                self.select_server(name),
                checked=lambda item, n=name: n == self.config_manager.data.get("active_server")
            ))
        return items

    def _get_interval_items(self):
        intervals = [
            ("⚡ 0.5s (Fast)", 0.5),
            ("⏱ 1.0s (Smooth)", 1.0),
            ("⏱ 1.5s (Default)", 1.5),
            ("⏱ 3.0s (Eco)", 3.0)
        ]
        items = []
        for label, val in intervals:
            items.append(item(
                label,
                self.select_interval(val),
                checked=lambda item, v=val: abs(self.config_manager.data.get("interval_seconds", 1.5) - v) < 0.05
            ))
        return items

    def build_menu(self):
        snap = self.last_snap or {}
        ping = snap.get("current")
        ping_str = f"{ping} ms" if ping is not None else "Timeout"
        avg_str = f"{snap.get('avg', 0)} ms"
        jitter_str = f"{snap.get('jitter', 0)} ms"
        loss_str = f"{snap.get('loss', 0)}%"

        active_name = self.config.get("active_server", "Target")

        menu_items = [
            item(f"{active_name}: {ping_str}", lambda icon, item: None, enabled=False),
            item(f"Avg: {avg_str} | Jitter: {jitter_str} | Loss: {loss_str}", lambda icon, item: None, enabled=False),
            item.SEPARATOR,
            item("🎯 Game Presets", Menu(*self._get_server_items())),
            item("⏱ Polling Rate", Menu(*self._get_interval_items())),
            item("⚙ Open config.json", self.open_config_file),
            item.SEPARATOR,
            item("Exit", self.exit_app)
        ]
        return Menu(*menu_items)

    def update_menu(self):
        if self.icon:
            self.icon.menu = self.build_menu()

    def run(self):
        self.pinger.start()
        initial_img = self.drawer.create_tray_icon(None)
        
        self.icon = pystray.Icon(
            name="TrayPingMonitor",
            icon=initial_img,
            title="Tray Ping Monitor",
            menu=self.build_menu()
        )
        self.icon.run()

if __name__ == "__main__":
    app = TrayPingApp()
    app.run()
