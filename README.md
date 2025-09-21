# PyTerm - Natural Language Terminal

A modern web-based terminal that understands natural language commands and converts them to traditional terminal operations.

🌐 **Live Demo**: [PyTerm on Vercel](https://python-based-command-terminal.vercel.app) *(Sandbox environment)*  
📥 **Download**: [Full Version](https://github.com/Kushal-V/Python-Based-Command-Terminal/releases) *(Access your real OS)*

## 🚀 Quick Start

### Option 1: Try Online (Sandbox)
Visit the live demo to test natural language commands in a safe environment.

### Option 2: Install Locally (Full OS Access)
```bash
# Windows
curl -O https://raw.githubusercontent.com/Kushal-V/Python-Based-Command-Terminal/main/install_local.bat
install_local.bat

# Linux/Mac
curl -O https://raw.githubusercontent.com/Kushal-V/Python-Based-Command-Terminal/main/install_local.sh
chmod +x install_local.sh
./install_local.sh
```

## ✨ Features

- 🗣️ **Natural Language Processing**: Type commands like "show me what's in this directory" or "create a folder called test"
- 🖥️ **Traditional Terminal Support**: All standard commands work (ls, cd, pwd, mkdir, rm)
- 🎨 **Modern UI**: Clean, minimal terminal interface
- 🔒 **Two Modes**: 
  - **Sandbox Mode**: Safe online demo
  - **Local Mode**: Full access to your computer
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🎯 How It Works

### Natural Language Examples:
| What You Type | What It Runs |
|---------------|--------------|
| "show me what's in this directory" | `ls` |
| "create a folder called my_files" | `mkdir my_files` |
| "go to the documents folder" | `cd documents` |
| "where am I right now?" | `pwd` |
| "delete the temp folder" | `rm temp` |

### Traditional Commands:
- `ls` - List files and directories
- `cd <directory>` - Change directory  
- `pwd` - Show current directory
- `mkdir <name>` - Create a directory
- `rm <path>` - Remove file or directory
- `history` - Show command history
- `clear` - Clear terminal
- `help` - Show help message

## 🌐 Deployment Options

### For Developers - Host Your Own:

#### Vercel (Recommended - Free):
```bash
git clone https://github.com/Kushal-V/Python-Based-Command-Terminal.git
cd Python-Based-Command-Terminal
# Push to your GitHub, then connect to Vercel
```

#### Alternative Platforms:
- **Railway**: Connect GitHub repo for auto-deployment
- **Heroku**: Use provided Procfile for deployment

### For Users - Local Installation:

#### Windows:
1. Download `install_local.bat`
2. Run it
3. Access at `http://localhost:5000`

#### Linux/Mac:
1. Download `install_local.sh`
2. Run: `chmod +x install_local.sh && ./install_local.sh`
3. Access at `http://localhost:5000`

## 🔒 Security & Permissions

### Online Version (Sandbox):
- ✅ Safe for public use
- ✅ Isolated temporary directories
- ❌ No access to real user files
- ✅ Perfect for learning/demos

### Local Installation:
- ✅ Full access to your computer
- ✅ Create real files and folders
- ✅ Navigate your actual directories
- ⚠️ Only install on trusted machines

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/Kushal-V/Python-Based-Command-Terminal.git
cd Python-Based-Command-Terminal

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Open browser
http://localhost:5000
```

## 📦 Project Structure

```
PyTerm/
├── app.py                 # Flask web application
├── main.py               # Terminal logic with interpret_command function
├── templates/
│   └── terminal.html     # Web interface
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
├── runtime.txt          # Python version for Heroku
├── install_local.bat    # Windows installer
├── install_local.sh     # Linux/Mac installer
├── DEPLOYMENT_GUIDE.md  # Detailed deployment instructions
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by modern terminal applications
- Built with Flask and vanilla JavaScript
- Natural language processing using custom pattern matching

---

**Made with ❤️ by [Kushal-V](https://github.com/Kushal-V)**
