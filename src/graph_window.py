import sys
import time
import ctypes
from ctypes import wintypes
import threading

# Win32 Constants
WS_POPUP = 0x80000000
WS_VISIBLE = 0x10000000
WS_EX_TOPMOST = 0x00000008
WS_EX_TOOLWINDOW = 0x00000080

WM_DESTROY = 0x0002
WM_PAINT = 0x000F
WM_TIMER = 0x0113
WM_LBUTTONDOWN = 0x0201
WM_RBUTTONDOWN = 0x0204
WM_KEYDOWN = 0x0100
WM_CLOSE = 0x0010

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

LRESULT = ctypes.c_longlong
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = LRESULT

user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.PostMessageW.restype = wintypes.BOOL

user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
user32.SetWindowPos.restype = wintypes.BOOL

class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HICON),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HICON)
    ]

class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG), ("right", wintypes.LONG), ("bottom", wintypes.LONG)]

class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", wintypes.BYTE * 32)
    ]

class MiniGraphWindow:
    _instance = None
    _lock = threading.Lock()
    _class_registered = False

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
        self.hwnd = None
        self.running = False
        self.thread = None
        self.wnd_proc_delegate = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_message_loop, daemon=True)
        self.thread.start()

    def is_alive(self):
        return self.running and self.hwnd is not None and user32.IsWindow(self.hwnd) != 0

    def bring_to_front(self):
        if self.hwnd and user32.IsWindow(self.hwnd):
            user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
            user32.SetForegroundWindow(self.hwnd)

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        try:
            if msg == WM_PAINT:
                ps = PAINTSTRUCT()
                hdc = user32.BeginPaint(hwnd, ctypes.byref(ps))
                self._on_paint(hwnd, hdc)
                user32.EndPaint(hwnd, ctypes.byref(ps))
                return 0

            elif msg == WM_TIMER:
                user32.InvalidateRect(hwnd, None, False)
                return 0

            elif msg == WM_LBUTTONDOWN:
                x = lparam & 0xFFFF
                y = (lparam >> 16) & 0xFFFF
                if x >= 300 and y <= 32:
                    user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
                return 0

            elif msg == WM_RBUTTONDOWN or msg == WM_KEYDOWN:
                if msg == WM_KEYDOWN and wparam != 27:
                    return 0
                user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
                return 0

            elif msg == WM_DESTROY:
                self.running = False
                self.hwnd = None
                user32.PostQuitMessage(0)
                return 0

            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        except Exception:
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _on_paint(self, hwnd, hdc):
        width, height = 330, 200

        mem_dc = gdi32.CreateCompatibleDC(hdc)
        mem_bmp = gdi32.CreateCompatibleBitmap(hdc, width, height)
        old_bmp = gdi32.SelectObject(mem_dc, mem_bmp)

        # 1. Background
        bg_brush = gdi32.CreateSolidBrush(0x001A1412)
        rc = RECT(0, 0, width, height)
        user32.FillRect(mem_dc, ctypes.byref(rc), bg_brush)
        gdi32.DeleteObject(bg_brush)

        # 2. Header Bar
        header_brush = gdi32.CreateSolidBrush(0x00221A18)
        rc_header = RECT(0, 0, width, 32)
        user32.FillRect(mem_dc, ctypes.byref(rc_header), header_brush)
        gdi32.DeleteObject(header_brush)

        gdi32.SetBkMode(mem_dc, 1)

        # Title
        snap = self.pinger.stats.get_snapshot() if self.pinger else {}
        active_name = self.config_manager.data.get("active_server", "Target") if self.config_manager else "Ping Monitor"
        resolved = snap.get("resolved_ip", "")
        title_text = f"{active_name}"
        if resolved and resolved not in active_name:
            title_text += f" [{resolved}]"

        gdi32.SetTextColor(mem_dc, 0x00FFFFFF)
        rc_title = RECT(12, 7, 295, 28)
        user32.DrawTextW(mem_dc, title_text[:38], -1, ctypes.byref(rc_title), 0x0000 | 0x0004)

        # Close X
        gdi32.SetTextColor(mem_dc, 0x00888888)
        rc_close = RECT(305, 6, 325, 26)
        user32.DrawTextW(mem_dc, "X", -1, ctypes.byref(rc_close), 0x0001 | 0x0004)

        # 3. Plot Area
        px_left, px_top, px_right, px_bottom = 12, 42, 318, 155
        plot_w = px_right - px_left
        plot_h = px_bottom - px_top

        plot_brush = gdi32.CreateSolidBrush(0x00120E0D)
        rc_plot = RECT(px_left, px_top, px_right, px_bottom)
        user32.FillRect(mem_dc, ctypes.byref(rc_plot), plot_brush)
        gdi32.DeleteObject(plot_brush)

        # Grid lines
        grid_pen = gdi32.CreatePen(0, 1, 0x002B1F1C)
        old_pen = gdi32.SelectObject(mem_dc, grid_pen)
        for ratio in [0.25, 0.5, 0.75]:
            gy = int(px_top + plot_h * ratio)
            gdi32.MoveToEx(mem_dc, px_left, gy, None)
            gdi32.LineTo(mem_dc, px_right, gy)
        gdi32.SelectObject(mem_dc, old_pen)
        gdi32.DeleteObject(grid_pen)

        # 4. Latency Line
        history = list(self.pinger.stats.history) if self.pinger else []
        if history:
            valid = [p for p in history if p is not None]
            max_val = max(max(valid, default=100.0) * 1.2, 80.0)
            step_x = plot_w / max(len(history) - 1, 1)

            line_pen = gdi32.CreatePen(0, 2, 0x0076E600) # Emerald Green BGR
            old_pen = gdi32.SelectObject(mem_dc, line_pen)

            first = True
            for i, val in enumerate(history):
                gx = int(px_left + i * step_x)
                if val is None:
                    drop_pen = gdi32.CreatePen(0, 2, 0x004444EF) # Red
                    gdi32.SelectObject(mem_dc, drop_pen)
                    gdi32.MoveToEx(mem_dc, gx, px_bottom - 8, None)
                    gdi32.LineTo(mem_dc, gx, px_bottom, None)
                    gdi32.SelectObject(mem_dc, line_pen)
                    gdi32.DeleteObject(drop_pen)
                    first = True
                else:
                    gy = int(px_bottom - (min(val, max_val) / max_val * plot_h))
                    if first:
                        gdi32.MoveToEx(mem_dc, gx, gy, None)
                        first = False
                    else:
                        gdi32.LineTo(mem_dc, gx, gy)

            gdi32.SelectObject(mem_dc, old_pen)
            gdi32.DeleteObject(line_pen)

        # 5. Border
        border_pen = gdi32.CreatePen(0, 1, 0x003D2E2A)
        old_pen = gdi32.SelectObject(mem_dc, border_pen)
        gdi32.MoveToEx(mem_dc, 0, 0, None)
        gdi32.LineTo(mem_dc, width - 1, 0)
        gdi32.LineTo(mem_dc, width - 1, height - 1)
        gdi32.LineTo(mem_dc, 0, height - 1)
        gdi32.LineTo(mem_dc, 0, 0)
        gdi32.SelectObject(mem_dc, old_pen)
        gdi32.DeleteObject(border_pen)

        # 6. Bottom Stats
        curr = snap.get('current')
        curr_str = f"{curr}ms" if curr is not None else "TIMEOUT"
        avg_str = f"{snap.get('avg', 0)}ms"
        jitter_str = f"{snap.get('jitter', 0)}ms"
        loss_str = f"{snap.get('loss', 0)}%"

        stats_text = f"Ping: {curr_str}   Avg: {avg_str}   Jitter: {jitter_str}   Loss: {loss_str}"
        gdi32.SetTextColor(mem_dc, 0x00AFB39C)
        rc_stats = RECT(10, 168, width - 10, 192)
        user32.DrawTextW(mem_dc, stats_text, -1, ctypes.byref(rc_stats), 0x0001 | 0x0004)

        gdi32.BitBlt(hdc, 0, 0, width, height, mem_dc, 0, 0, 0x00CC0020)

        gdi32.SelectObject(mem_dc, old_bmp)
        gdi32.DeleteObject(mem_bmp)
        gdi32.DeleteDC(mem_dc)

    def _run_message_loop(self):
        h_instance = kernel32.GetModuleHandleW(None)
        class_name = "TrayPingMonitor_Win32Graph"

        if not MiniGraphWindow._class_registered:
            self.wnd_proc_delegate = WNDPROC(self._wnd_proc)
            wcex = WNDCLASSEXW()
            wcex.cbSize = ctypes.sizeof(WNDCLASSEXW)
            wcex.style = 0x0003
            wcex.lpfnWndProc = self.wnd_proc_delegate
            wcex.cbClsExtra = 0
            wcex.cbWndExtra = 0
            wcex.hInstance = h_instance
            wcex.hIcon = 0
            wcex.hCursor = user32.LoadCursorW(0, 32512)
            wcex.hbrBackground = 0
            wcex.lpszMenuName = None
            wcex.lpszClassName = class_name
            wcex.hIconSm = 0

            user32.RegisterClassExW(ctypes.byref(wcex))
            MiniGraphWindow._class_registered = True

        width, height = 330, 200
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        x = sw - width - 20
        y = sh - height - 60

        self.hwnd = user32.CreateWindowExW(
            WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
            class_name,
            "Ping Monitor",
            WS_POPUP | WS_VISIBLE,
            x, y, width, height,
            0, 0, h_instance, None
        )

        if not self.hwnd:
            self.running = False
            return

        user32.SetTimer(self.hwnd, 1, 300, None)
        user32.ShowWindow(self.hwnd, 5)
        user32.UpdateWindow(self.hwnd)
        user32.SetForegroundWindow(self.hwnd)

        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        self.running = False
        self.hwnd = None
