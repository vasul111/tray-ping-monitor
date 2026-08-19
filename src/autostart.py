import sys
import winreg
from pathlib import Path

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "TrayPingMonitor"

def get_target_path() -> str:
    if getattr(sys, 'frozen', False):
        return f'"{sys.executable}"'
    python_exe = sys.executable
    main_py = Path(__file__).resolve().parent / "main.py"
    return f'"{python_exe}" "{main_py}"'

def is_autostart_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

def set_autostart(enable: bool) -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ) as key:
            if enable:
                target = get_target_path()
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, target)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
        return True
    except Exception as e:
        print(f"Error setting autostart: {e}")
        return False
