import time
import socket
import threading
from collections import deque
import ping3
from src.roblox_detector import RobloxServerDetector
from src.cs2_detector import CS2ServerDetector

class PingStats:
    def __init__(self, history_size: int = 40):
        self.history_size = history_size
        self.lock = threading.Lock()
        self.history = deque(maxlen=history_size)
        self.current_ping = None
        self.avg_ping = 0.0
        self.min_ping = 0.0
        self.max_ping = 0.0
        self.jitter = 0.0
        self.loss_pct = 0.0
        self.last_update = 0.0
        self.resolved_ip = ""

    def record(self, ping_ms: float | None, resolved_ip: str = ""):
        with self.lock:
            self.current_ping = ping_ms
            self.history.append(ping_ms)
            self.last_update = time.time()
            self.resolved_ip = resolved_ip

            valid = [p for p in self.history if p is not None]
            total = len(self.history)
            lost = total - len(valid)

            self.loss_pct = round((lost / total) * 100, 1) if total > 0 else 0.0

            if valid:
                self.avg_ping = round(sum(valid) / len(valid), 1)
                self.min_ping = round(min(valid), 1)
                self.max_ping = round(max(valid), 1)

                if len(valid) > 1:
                    diffs = [abs(valid[i] - valid[i - 1]) for i in range(1, len(valid))]
                    self.jitter = round(sum(diffs) / len(diffs), 1)
                else:
                    self.jitter = 0.0
            else:
                self.avg_ping = 0.0
                self.min_ping = 0.0
                self.max_ping = 0.0
                self.jitter = 0.0

    def get_snapshot(self) -> dict:
        with self.lock:
            return {
                "current": self.current_ping,
                "avg": self.avg_ping,
                "min": self.min_ping,
                "max": self.max_ping,
                "jitter": self.jitter,
                "loss": self.loss_pct,
                "resolved_ip": self.resolved_ip,
                "last_update": self.last_update,
                "samples_count": len(self.history)
            }


class BackgroundPinger:
    def __init__(self, host: str, interval: float = 1.5, history_size: int = 40, on_update_callback=None):
        self.host = host
        self.interval = interval
        self.stats = PingStats(history_size=history_size)
        self.on_update_callback = on_update_callback
        self.running = False
        self._thread = None
        self.roblox_detector = RobloxServerDetector()
        self.cs2_detector = CS2ServerDetector()

    def set_target(self, host: str):
        if self.host != host:
            self.host = host
            with self.stats.lock:
                self.stats.history.clear()
                self.stats.current_ping = None

    def set_interval(self, interval: float):
        self.interval = max(0.3, float(interval))

    def _resolve_target_host(self) -> tuple[str, int, str]:
        host = self.host
        port = 443

        if host == "auto:roblox":
            ip, status = self.roblox_detector.get_latest_server_ip()
            if ip:
                return ip, 443, f"Live: {ip}"
            return "ec2.eu-central-1.amazonaws.com", 443, "Standby (EU)"

        if host == "auto:cs2":
            ip, status = self.cs2_detector.get_latest_server_ip()
            if ip:
                return ip, 27015, f"Live: {ip}"
            return "fra.valve.net", 443, "Standby (Frankfurt SDR)"

        if ":" in host and not host.startswith("auto:"):
            parts = host.split(":")
            host = parts[0]
            try:
                port = int(parts[1])
            except ValueError:
                port = 443

        return host, port, host

    def _ping_target(self, host: str, port: int) -> float | None:
        try:
            val = ping3.ping(host, unit='ms', timeout=1.0)
            if val is not None and val is not False:
                return round(float(val), 1)
        except Exception:
            pass

        t0 = time.perf_counter()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.2)
            sock.connect((host, port))
            sock.close()
            return round((time.perf_counter() - t0) * 1000.0, 1)
        except Exception:
            return None

    def _worker(self):
        while self.running:
            t0 = time.time()
            target_host, target_port, target_label = self._resolve_target_host()

            res = self._ping_target(target_host, target_port)
            self.stats.record(res, resolved_ip=target_label)

            if self.on_update_callback:
                try:
                    self.on_update_callback(self.stats.get_snapshot())
                except Exception:
                    pass

            elapsed = time.time() - t0
            time.sleep(max(0.05, self.interval - elapsed))

    def start(self):
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.5)
