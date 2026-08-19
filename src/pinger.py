import time
import threading
from collections import deque
import ping3

class PingStats:
    def __init__(self, history_size: int = 30):
        self.history_size = history_size
        self.lock = threading.Lock()
        self.history = deque(maxlen=history_size)  # stores float (ms) or None (loss)
        self.current_ping = None
        self.avg_ping = 0.0
        self.min_ping = 0.0
        self.max_ping = 0.0
        self.jitter = 0.0
        self.loss_pct = 0.0
        self.last_update = 0.0
        self.status = "INITIALIZING"

    def record(self, ping_ms: float | None):
        with self.lock:
            self.current_ping = ping_ms
            self.history.append(ping_ms)
            self.last_update = time.time()

            # Calculate stats over rolling window
            valid_pings = [p for p in self.history if p is not None]
            total_samples = len(self.history)
            lost_samples = total_samples - len(valid_pings)

            if total_samples > 0:
                self.loss_pct = round((lost_samples / total_samples) * 100, 1)
            else:
                self.loss_pct = 0.0

            if valid_pings:
                self.avg_ping = round(sum(valid_pings) / len(valid_pings), 1)
                self.min_ping = round(min(valid_pings), 1)
                self.max_ping = round(max(valid_pings), 1)

                # Jitter calculation: average difference between consecutive valid samples
                if len(valid_pings) > 1:
                    diffs = [abs(valid_pings[i] - valid_pings[i - 1]) for i in range(1, len(valid_pings))]
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
            # Clear previous history when target changes
            with self.stats.lock:
                self.stats.history.clear()
                self.stats.current_ping = None

    def set_interval(self, interval: float):
        self.interval = max(0.5, float(interval))

    def _ping_loop(self):
        while self.running:
            start_time = time.time()
            res = None
            try:
                # ping3 returns float in ms when unit='ms', or None on timeout/False on error
                val = ping3.ping(self.host, unit='ms', timeout=1.2)
                if val is not None and val is not False:
                    res = round(float(val), 1)
                else:
                    res = None
            except Exception as e:
                res = None

            self.stats.record(res)

            if self.on_update_callback:
                try:
                    self.on_update_callback(self.stats.get_snapshot())
                except Exception:
                    pass

            elapsed = time.time() - start_time
            sleep_time = max(0.1, self.interval - elapsed)
            time.sleep(sleep_time)

    def start(self):
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._ping_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
