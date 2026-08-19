import tkinter as tk
import threading
import time

class MiniGraphWindow:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def show_graph(cls, pinger_ref, config_manager_ref):
        with cls._lock:
            if cls._instance and cls._instance.is_alive():
                cls._instance.bring_to_front()
                return

            cls._instance = MiniGraphWindow(pinger_ref, config_manager_ref)
            cls._instance.start()

    def __init__(self, pinger, config_manager):
        self.pinger = pinger
        self.config_manager = config_manager
        self.root = None
        self.canvas = None
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_ui, daemon=True)
        self.thread.start()

    def is_alive(self):
        return self.running and self.root is not None

    def bring_to_front(self):
        if self.root:
            try:
                self.root.lift()
                self.root.attributes('-topmost', True)
            except Exception:
                pass

    def _close(self, event=None):
        self.running = False
        if self.root:
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None

    def _run_ui(self):
        self.root = tk.Tk()
        self.root.title("Ping Monitor")
        self.root.overrideredirect(True)  # Frameless modern window
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#12141a")

        w, h = 330, 200
        # Position at bottom-right near tray
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - w - 20
        y = sh - h - 60
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Bind events to close
        self.root.bind("<FocusOut>", self._close)
        self.root.bind("<Escape>", self._close)
        self.root.bind("<Button-3>", self._close)  # Right click to close

        # Top Header Frame
        header = tk.Frame(self.root, bg="#181a22", height=32)
        header.pack(fill="x", side="top")

        self.lbl_title = tk.Label(header, text="Live Network Latency", font=("Segoe UI", 9, "bold"), fg="#e0e0e0", bg="#181a22")
        self.lbl_title.pack(side="left", padx=10, pady=6)

        btn_close = tk.Label(header, text="✕", font=("Segoe UI", 9, "bold"), fg="#888", bg="#181a22", cursor="hand2")
        btn_close.pack(side="right", padx=10, pady=6)
        btn_close.bind("<Button-1>", self._close)

        # Graph Canvas
        self.canvas = tk.Canvas(self.root, width=310, height=105, bg="#0d0e12", highlightthickness=1, highlightbackground="#252836")
        self.canvas.pack(padx=10, pady=8)

        # Bottom Stats Bar
        self.lbl_stats = tk.Label(self.root, text="Loading stats...", font=("Segoe UI", 8), fg="#9ca3af", bg="#12141a")
        self.lbl_stats.pack(side="bottom", pady=4)

        self._update_loop()
        self.root.mainloop()

    def _update_loop(self):
        if not self.running or not self.root:
            return

        try:
            snap = self.pinger.stats.get_snapshot()
            active_name = self.config_manager.data.get("active_server", "Target")
            resolved = snap.get("resolved_ip", "")
            
            title_text = f"{active_name}"
            if resolved and resolved not in active_name:
                title_text += f" [{resolved}]"
            self.lbl_title.config(text=title_text[:36])

            # Draw Graph
            self._draw_graph(snap)

            # Update text stats
            curr = snap.get('current')
            curr_str = f"{curr}ms" if curr is not None else "TIMEOUT"
            avg_str = f"{snap.get('avg', 0)}ms"
            jitter_str = f"{snap.get('jitter', 0)}ms"
            loss_str = f"{snap.get('loss', 0)}%"

            self.lbl_stats.config(text=f"Ping: {curr_str}  |  Avg: {avg_str}  |  Jitter: {jitter_str}  |  Loss: {loss_str}")

            self.root.after(300, self._update_loop)
        except Exception:
            self._close()

    def _draw_graph(self, snap):
        if not self.canvas:
            return

        self.canvas.delete("all")
        history = list(self.pinger.stats.history)
        if not history:
            return

        cw, ch = 310, 105
        pad_x, pad_y = 12, 10
        plot_w = cw - (pad_x * 2)
        plot_h = ch - (pad_y * 2)

        # Draw grid lines
        for y_ratio in [0.25, 0.5, 0.75]:
            gy = pad_y + plot_h * y_ratio
            self.canvas.create_line(pad_x, gy, cw - pad_x, gy, fill="#1c1f2b", dash=(2, 4))

        valid = [p for p in history if p is not None]
        max_val = max(max(valid, default=100.0) * 1.2, 80.0)

        step_x = plot_w / max(len(history) - 1, 1)

        points = []
        for i, val in enumerate(history):
            px = pad_x + i * step_x
            if val is None:
                py = pad_y + plot_h
                # Mark loss with small red cross
                self.canvas.create_line(px - 3, py - 6, px + 3, py, fill="#ef4444", width=2)
                self.canvas.create_line(px - 3, py, px + 3, py - 6, fill="#ef4444", width=2)
            else:
                py = pad_y + plot_h - (min(val, max_val) / max_val * plot_h)
                points.append((px, py))

        # Draw connecting line
        if len(points) > 1:
            line_coords = []
            for px, py in points:
                line_coords.extend([px, py])
            self.canvas.create_line(line_coords, fill="#00e676", width=2, smooth=True)

        # Draw dots on points
        for px, py in points:
            self.canvas.create_oval(px - 2, py - 2, px + 2, py + 2, fill="#ffffff", outline="#00e676")
