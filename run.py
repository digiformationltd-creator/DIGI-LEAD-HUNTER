# Digiformation LTD — Lead Hunter
# Universal 1-Click Runner & Antigravity Launcher
import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend" / "app"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

def main():
    print("=" * 65)
    print("  DIGI LEAD HUNTER — LOCAL BUSINESS INTELLIGENCE AGENT")
    print("  by Digiformation LTD • Sponsored by Digi Biz OS")
    print("=" * 65)

    # 1. Initialize Database
    sys.path.append(str(BACKEND_DIR))
    from database import init_db
    print("\n[1/4] Initializing SQLite database...")
    init_db()
    print("  -> Database ready.")

    # 2. Check Frontend Build
    print("\n[2/4] Verifying Control Center frontend build...")
    if not (FRONTEND_DIST / "index.html").exists():
        print("  -> Building frontend distribution assets...")
        frontend_dir = BASE_DIR / "frontend"
        subprocess.run(["cmd.exe", "/c", "npm.cmd run build"], cwd=str(frontend_dir), shell=True)
    print("  -> Frontend assets verified.")

    # 3. Open Browser
    url = "http://127.0.0.1:8000"
    print(f"\n[3/4] Launching Control Center in browser: {url}")
    webbrowser.open(url)

    # 4. Start Server
    print("\n[4/4] Starting FastAPI backend server...")
    print("  Local URL: " + url)
    print("  WhatsApp Support: +92 316 4467464 (03164467464)")
    print("  Press Ctrl+C anytime to stop.")
    print("=" * 65 + "\n")

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
