@echo off
REM PyTerm Local Installation Script for Windows

echo 🚀 Installing PyTerm - Natural Language Terminal
echo This will install PyTerm locally for full OS access
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Install Flask
echo 📦 Installing dependencies...
pip install flask

REM Create startup script
echo import subprocess > start_pyterm.py
echo import webbrowser >> start_pyterm.py
echo import time >> start_pyterm.py
echo import threading >> start_pyterm.py
echo import sys >> start_pyterm.py
echo. >> start_pyterm.py
echo def start_server(): >> start_pyterm.py
echo     subprocess.run([sys.executable, "app.py"]) >> start_pyterm.py
echo. >> start_pyterm.py
echo def open_browser(): >> start_pyterm.py
echo     time.sleep(2) >> start_pyterm.py
echo     webbrowser.open('http://localhost:5000') >> start_pyterm.py
echo. >> start_pyterm.py
echo if __name__ == "__main__": >> start_pyterm.py
echo     server_thread = threading.Thread(target=start_server) >> start_pyterm.py
echo     server_thread.daemon = True >> start_pyterm.py
echo     server_thread.start() >> start_pyterm.py
echo     open_browser() >> start_pyterm.py
echo     print("PyTerm is running! Close this window to stop the server.") >> start_pyterm.py
echo     try: >> start_pyterm.py
echo         server_thread.join() >> start_pyterm.py
echo     except KeyboardInterrupt: >> start_pyterm.py
echo         print("\nShutting down PyTerm...") >> start_pyterm.py

echo.
echo ✅ Installation complete!
echo.
echo 🎯 To start PyTerm:
echo    python start_pyterm.py
echo.
echo    Or manually:
echo    python app.py
echo    Then open: http://localhost:5000
echo.
echo 📁 PyTerm will have full access to your file system
echo 🔒 This is safe since it's running on your own computer
pause
