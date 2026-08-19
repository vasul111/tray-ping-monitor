import os
import sys
import subprocess

def build():
    print("🚀 Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    print("🔨 Building standalone .exe...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=TrayPingMonitor",
        "--clean",
        "src/main.py"
    ]
    subprocess.check_call(cmd)
    print("\n✅ Build complete! Executable is located in the 'dist' folder: dist/TrayPingMonitor.exe")

if __name__ == "__main__":
    build()
