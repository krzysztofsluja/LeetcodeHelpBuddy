@echo off
REM Activate virtual environment for Windows Command Prompt
echo 🐍 Activating LeetCode Help Buddy virtual environment...
call leetcode_env\Scripts\activate.bat
echo ✅ Virtual environment activated!
echo.
echo 📋 Available commands:
echo   python run.py           - Run the app with hot reload
echo   python run_venv.py      - Run using venv (alternative)
echo   pip install package     - Install new packages
echo   deactivate             - Exit virtual environment
echo.
cmd /k
