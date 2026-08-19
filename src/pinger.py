import time
import threading
from collections import deque
import ping3

class PingStats:
    def __init__(self, history_size: int = 30):
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

    def record(self, ping_ms: float | None):
        with self.lock:
            self.current_ping = ping_ms
            self.history.append(ping_ms)
            self.last_update = time.time()

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
                "last_update": self.last_update,
                "samples_count": len(self.history)
            }


class BackgroundPinger:
    def __init__(self, host: str, interval: float = 1.5, history_size: int = 30, on_update_callback=None):
        self.host = host
        self.interval = interval
        self.stats = PingStats(history_size=history_size)
        self.on_update_callback = on_update_callback
        self.running = False
        self._thread = None

    def set_target(self, host: str):
        if self.host != host:
            self.host = host
            with self.stats.lock:
                self.stats.history.clear()
                self.stats.current_ping = None

    def set_interval(self, interval: float):
        self.interval = max(0.3, float(interval))

    def _worker(self):
        while self.running:
            t0 = time.time()
            res = None
            try:
                val = ping3.ping(self.host, unit='ms', timeout=1.2)
                if val is not None and val is not False:
                    res = round(float(val), 1)
            except Exception:
                res = None

            self.stats.record(res)

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
