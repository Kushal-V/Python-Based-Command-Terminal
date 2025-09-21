#!/bin/bash
# PyTerm Local Installation Script

echo "🚀 Installing PyTerm - Natural Language Terminal"
echo "This will install PyTerm locally for full OS access"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "✅ Python 3 found"

# Install Flask
echo "📦 Installing dependencies..."
pip3 install flask

# Create desktop shortcut script
cat > start_pyterm.py << 'EOF'
import subprocess
import webbrowser
import time
import threading
import sys
import os

def start_server():
    subprocess.run([sys.executable, "app.py"])

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    # Start server in background
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser
    open_browser()
    
    print("PyTerm is running! Close this window to stop the server.")
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down PyTerm...")
EOF

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 To start PyTerm:"
echo "   python3 start_pyterm.py"
echo ""
echo "   Or manually:"
echo "   python3 app.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "📁 PyTerm will have full access to your file system"
echo "🔒 This is safe since it's running on your own computer"
