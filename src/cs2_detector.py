import psutil

class CS2ServerDetector:
    def __init__(self):
        # Known Valve SDR network IP prefixes
        self.valve_prefixes = ("162.254.", "155.133.", "185.25.", "146.66.")

    def get_latest_server_ip(self) -> tuple[str | None, str]:
        cs2_procs = []
        try:
            for p in psutil.process_iter(['name', 'pid']):
                pname = (p.info.get('name') or "").lower()
                if pname in ("cs2.exe", "csgo.exe", "dota2.exe"):
                    cs2_procs.append(p)
        except Exception:
            return None, "CS2: Not Running"

        if not cs2_procs:
            return None, "CS2: Not Running"

        for proc in cs2_procs:
            try:
                connections = proc.net_connections(kind='inet')
                # Check for active UDP/TCP game connections
                for conn in connections:
                    raddr = conn.raddr
                    if raddr and raddr.ip:
                        ip = raddr.ip
                        port = raddr.port
                        # Check Valve SDR or game server ports
                        if any(ip.startswith(prefix) for prefix in self.valve_prefixes) or (27000 <= port <= 27080):
                            if ip != "127.0.0.1" and not ip.startswith("192.168."):
                                return ip, f"CS2 Live: {ip}"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            except Exception:
                continue

        return None, "CS2: In Lobby / Searching"
