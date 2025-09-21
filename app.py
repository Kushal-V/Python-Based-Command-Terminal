from flask import Flask, render_template, request, jsonify, session
import os
import shutil
import tempfile
import uuid
import platform
from main import interpret_command
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Store user sessions and their virtual file systems
user_sessions = {}

# Detect if we're running on a serverless platform or locally
def is_serverless_environment():
    """Detect if running on serverless platform (Vercel, Heroku, etc.)"""
    return (
        os.environ.get('VERCEL') or 
        os.environ.get('DYNO') or 
        os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or
        '/var/task' in os.getcwd() or
        '/tmp' in tempfile.gettempdir() or
        os.access(os.getcwd(), os.W_OK) == False
    )

class FileSystemManager:
    def __init__(self):
        self.is_serverless = is_serverless_environment()
        if self.is_serverless:
            # Virtual file system for serverless
            self.base_dir = tempfile.mkdtemp()
            self.current_dir = self.base_dir
            self.mode = "SANDBOX"
        else:
            # Real file system for local
            self.base_dir = os.getcwd()
            self.current_dir = self.base_dir
            self.mode = "REAL OS"
        
        self.history = []
        
    def get_relative_path(self):
        """Get the current path relative to the base directory"""
        if self.current_dir == self.base_dir:
            return "~"
        try:
            rel_path = os.path.relpath(self.current_dir, self.base_dir)
            return f"~/{rel_path}"
        except ValueError:
            # Handle different drives on Windows
            return self.current_dir
    
    def get_mode_info(self):
        """Get information about current mode"""
        if self.is_serverless:
            return {
                "mode": "SANDBOX",
                "description": "Virtual file system - safe for demonstrations",
                "warning": "Files are temporary and will be lost when session ends"
            }
        else:
            return {
                "mode": "REAL OS",
                "description": "Direct access to your actual file system",
                "warning": "Commands will create/modify real files on your computer"
            }
    
    def is_path_safe(self, path):
        """Check if path is safe for operations"""
        if self.is_serverless:
            # In serverless, restrict to temp directory
            abs_path = os.path.abspath(os.path.join(self.current_dir, path))
            return abs_path.startswith(self.base_dir)
        else:
            # Local mode - more permissive but still some restrictions
            restricted_paths = [
                '/etc', '/sys', '/proc', '/dev', 
                'C:\\Windows', 'C:\\System32', 'C:\\Program Files'
            ]
            abs_path = os.path.abspath(os.path.join(self.current_dir, path))
            return not any(abs_path.startswith(restricted) for restricted in restricted_paths)
    
    def execute_command(self, command_str):
        """Execute a command in the file system"""
        try:
            if not command_str.strip():
                return {"output": "", "error": "", "success": True}
            
            parts = command_str.split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if command == "pwd":
                if self.is_serverless:
                    return {"output": self.get_relative_path(), "error": "", "success": True}
                else:
                    return {"output": os.getcwd(), "error": "", "success": True}
            
            elif command == "ls":
                try:
                    items = os.listdir(self.current_dir)
                    if not items:
                        return {"output": "(empty directory)", "error": "", "success": True}
                    output = "\n".join(sorted(items))
                    return {"output": output, "error": "", "success": True}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "cd":
                try:
                    if not args:
                        if self.is_serverless:
                            self.current_dir = self.base_dir
                        else:
                            self.current_dir = os.path.expanduser('~')
                            os.chdir(self.current_dir)
                        return {"output": "", "error": "", "success": True}
                    
                    target = args[0].strip('"\'')
                    if target == "..":
                        parent = os.path.dirname(self.current_dir)
                        if self.is_serverless:
                            # Don't go above base directory in serverless
                            if len(parent) >= len(self.base_dir):
                                self.current_dir = parent
                        else:
                            self.current_dir = parent
                            os.chdir(self.current_dir)
                    elif target == "~":
                        if self.is_serverless:
                            self.current_dir = self.base_dir
                        else:
                            self.current_dir = os.path.expanduser('~')
                            os.chdir(self.current_dir)
                    else:
                        new_path = os.path.join(self.current_dir, target)
                        if os.path.exists(new_path) and os.path.isdir(new_path):
                            if self.is_path_safe(target):
                                self.current_dir = os.path.abspath(new_path)
                                if not self.is_serverless:
                                    os.chdir(self.current_dir)
                            else:
                                return {"output": "", "error": f"Error: Access denied to {target}", "success": False}
                        else:
                            return {"output": "", "error": f"Error: Directory not found: {target}", "success": False}
                    
                    return {"output": "", "error": "", "success": True}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "mkdir":
                try:
                    if not args:
                        return {"output": "", "error": "Error: Please specify a directory name.", "success": False}
                    
                    dir_name = args[0].strip('"\'')
                    if not self.is_path_safe(dir_name):
                        return {"output": "", "error": f"Error: Access denied to {dir_name}", "success": False}
                    
                    new_path = os.path.join(self.current_dir, dir_name)
                    os.makedirs(new_path, exist_ok=False)
                    return {"output": f"Directory '{dir_name}' created.", "error": "", "success": True}
                except FileExistsError:
                    return {"output": "", "error": f"Error: Directory already exists: {args[0]}", "success": False}
                except PermissionError:
                    if self.is_serverless:
                        return {"output": "", "error": "Error: File system is read-only in demo mode. Download local version for full functionality.", "success": False}
                    else:
                        return {"output": "", "error": f"Error: Permission denied", "success": False}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "rm":
                try:
                    if not args:
                        return {"output": "", "error": "Error: Please specify a file or directory to remove.", "success": False}
                    
                    target = args[0].strip('"\'')
                    if not self.is_path_safe(target):
                        return {"output": "", "error": f"Error: Access denied to {target}", "success": False}
                    
                    target_path = os.path.join(self.current_dir, target)
                    
                    if os.path.isfile(target_path):
                        os.remove(target_path)
                        return {"output": f"File '{target}' removed.", "error": "", "success": True}
                    elif os.path.isdir(target_path):
                        shutil.rmtree(target_path)
                        return {"output": f"Directory '{target}' removed.", "error": "", "success": True}
                    else:
                        return {"output": "", "error": f"Error: File or directory not found: {target}", "success": False}
                except PermissionError:
                    if self.is_serverless:
                        return {"output": "", "error": "Error: File system is read-only in demo mode. Download local version for full functionality.", "success": False}
                    else:
                        return {"output": "", "error": f"Error: Permission denied", "success": False}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "history":
                if not self.history:
                    return {"output": "(no commands in history)", "error": "", "success": True}
                output = "\n".join([f"{i+1:>3}: {cmd}" for i, cmd in enumerate(self.history)])
                return {"output": output, "error": "", "success": True}
            
            elif command == "clear":
                return {"output": "CLEAR_TERMINAL", "error": "", "success": True}
            
            elif command == "mode":
                mode_info = self.get_mode_info()
                output = f"Mode: {mode_info['mode']}\n"
                output += f"Description: {mode_info['description']}\n"
                output += f"Note: {mode_info['warning']}"
                return {"output": output, "error": "", "success": True}
            
            elif command == "help":
                mode_info = self.get_mode_info()
                help_text = f"""Available commands:
ls - List files and directories
cd <directory> - Change directory
pwd - Show current directory
mkdir <name> - Create a directory
rm <path> - Remove file or directory
history - Show command history
clear - Clear terminal
mode - Show current mode information
help - Show this help message

Current Mode: {mode_info['mode']}
{mode_info['description']}

You can also use natural language! Try:
- "show me what's in this directory"
- "create a folder called test"
- "go to the documents folder"
- "where am I right now?"
- "delete the temp folder"

{'Note: ' + mode_info['warning']}"""
                return {"output": help_text, "error": "", "success": True}
            
            else:
                return {"output": "", "error": f"Error: Command '{command}' not found. Type 'help' for available commands.", "success": False}
        
        except Exception as e:
            return {"output": "", "error": f"Error: {str(e)}", "success": False}

def get_user_session():
    """Get or create a user session"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    if session_id not in user_sessions:
        user_sessions[session_id] = FileSystemManager()
    
    return user_sessions[session_id]

@app.route('/')
def index():
    return render_template('terminal.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        data = request.get_json()
        user_input = data.get('command', '').strip()
        
        if not user_input:
            return jsonify({"output": "", "error": "", "success": True, "prompt": ""})
        
        # Get user session
        user_fs = get_user_session()
        
        # Add to history
        user_fs.history.append(user_input)
        
        # Handle special commands
        if user_input.lower() == 'exit':
            return jsonify({
                "output": "Thanks for using PyTerm! Refresh to start a new session.",
                "error": "",
                "success": True,
                "prompt": user_fs.get_relative_path(),
                "mode": user_fs.get_mode_info()
            })
        
        # Try to interpret the command using natural language
        interpreted = interpret_command(user_input)
        final_command = interpreted if interpreted else user_input
        
        # Execute the command
        result = user_fs.execute_command(final_command)
        result["prompt"] = user_fs.get_relative_path()
        result["mode"] = user_fs.get_mode_info()
        
        # Show interpretation if it was used
        if interpreted and interpreted != user_input:
            result["interpretation"] = f"Interpreted as: {interpreted}"
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "output": "",
            "error": f"Server error: {str(e)}",
            "success": False,
            "prompt": "~",
            "mode": {"mode": "ERROR", "description": "System error"}
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# For Vercel deployment
app = app
