# Activate virtual environment for PowerShell
Write-Host "🐍 Activating LeetCode Help Buddy virtual environment..." -ForegroundColor Green

try {
    & ".\leetcode_env\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Available commands:" -ForegroundColor Yellow
    Write-Host "  python run.py           - Run the app with hot reload"
    Write-Host "  python run_venv.py      - Run using venv (alternative)"  
    Write-Host "  pip install package     - Install new packages"
    Write-Host "  deactivate             - Exit virtual environment"
    Write-Host ""
}
catch {
    Write-Host "❌ Could not activate virtual environment." -ForegroundColor Red
    Write-Host "This might be due to PowerShell execution policy." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "1. Use Command Prompt instead: double-click activate_venv.bat"
    Write-Host "2. Or run directly: python run_venv.py"
    Write-Host "3. Or change execution policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
}
