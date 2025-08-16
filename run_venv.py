#!/usr/bin/env python3
"""
Run the LeetCode Help Buddy app using the virtual environment.

This script automatically uses the virtual environment's Python interpreter.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the app with the virtual environment's Python."""
    project_root = Path(__file__).parent
    
    # Path to virtual environment Python
    if sys.platform == "win32":
        venv_python = project_root / "leetcode_env" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / "leetcode_env" / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv leetcode_env")
        print("Then install dependencies: leetcode_env\\Scripts\\pip.exe install -r requirements.txt")
        return 1
    
    print("🚀 Starting LeetCode Help Buddy with virtual environment...")
    
    # Run uvicorn with the virtual environment's Python
    try:
        subprocess.run([
            str(venv_python), "-m", "uvicorn",
            "app.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 LeetCode Help Buddy stopped.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running the app: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
