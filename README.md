# PyTerm - Natural Language Terminal

A modern web-based terminal that understands natural language commands and converts them to traditional terminal operations.

## Features

- 🗣️ **Natural Language Processing**: Type commands like "show me what's in this directory" or "create a folder called test"
- 🖥️ **Traditional Terminal Support**: All standard commands work (ls, cd, pwd, mkdir, rm)
- 🎨 **Modern UI**: Beautiful terminal interface with syntax highlighting
- 🔒 **Isolated Sessions**: Each user gets their own virtual file system
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Available Commands

### Natural Language Examples:
- "show me what's in this directory" → `ls`
- "create a folder called my_files" → `mkdir my_files`
- "go to the documents folder" → `cd documents`
- "where am I right now?" → `pwd`
- "delete the temp folder" → `rm temp`

### Traditional Commands:
- `ls` - List files and directories
- `cd <directory>` - Change directory
- `pwd` - Show current directory
- `mkdir <name>` - Create a directory
- `rm <path>` - Remove file or directory
- `history` - Show command history
- `clear` - Clear terminal
- `help` - Show help message

## Local Development

1. Install Python 3.7+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

## Deployment

### Heroku
1. Install Heroku CLI
2. Create a new Heroku app
3. Deploy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-app-name
   git push heroku main
   ```

### Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect and deploy the Flask app

### DigitalOcean App Platform
1. Create a new app from your GitHub repository
2. Configure the build and run commands in the app settings

## Project Structure

```
PyTerm/
├── app.py              # Flask web application
├── main.py             # Original terminal logic with interpret_command function
├── templates/
│   └── terminal.html   # Web interface
├── requirements.txt    # Python dependencies
├── Procfile           # For Heroku deployment
└── README.md          # This file
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with terminal theme
- **NLP**: Custom pattern matching for command interpretation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for learning or commercial purposes.
