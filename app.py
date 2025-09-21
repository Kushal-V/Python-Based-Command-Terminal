from flask import Flask, render_template, request, jsonify, session
import os
import shutil
import uuid
from main import interpret_command
import threading
import time
import platform

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Store user sessions and their current working directories
user_sessions = {}

class RealFileSystem:
    def __init__(self):
        # Start in the application directory for safety
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_dir = self.base_dir
        self.history = []
        
    def get_current_path(self):
        """Get the current directory path"""
        return self.current_dir
    
    def get_display_path(self):
        """Get a user-friendly display of the current path"""
        if platform.system() == "Windows":
            return self.current_dir.replace("\\", "/")
        return self.current_dir
    
    
    def is_safe_path(self, path):
        """Check if the path is safe to operate on (security measure)"""
        try:
            # Get the absolute path
            abs_path = os.path.abspath(path)
            
            # Allow operations in the application directory and subdirectories
            app_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Allow operations in user's home directory and subdirectories
            home_dir = os.path.expanduser("~")
            
            # Check if path is within allowed directories
            return (abs_path.startswith(app_dir) or 
                   abs_path.startswith(home_dir) or
                   abs_path.startswith(os.getcwd()))
        except:
            return False
    
    def execute_command(self, command_str):
        """Execute a command in the real file system"""
        try:
            if not command_str.strip():
                return {"output": "", "error": "", "success": True}
            
            parts = command_str.split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if command == "pwd":
                return {"output": self.get_display_path(), "error": "", "success": True}
            
            elif command == "ls":
                try:
                    if not self.is_safe_path(self.current_dir):
                        return {"output": "", "error": "Error: Access denied to this directory", "success": False}
                    
                    items = os.listdir(self.current_dir)
                    if not items:
                        return {"output": "(empty directory)", "error": "", "success": True}
                    
                    # Sort items and add indicators for directories
                    sorted_items = []
                    for item in sorted(items):
                        item_path = os.path.join(self.current_dir, item)
                        if os.path.isdir(item_path):
                            sorted_items.append(f"{item}/")
                        else:
                            sorted_items.append(item)
                    
                    output = "\n".join(sorted_items)
                    return {"output": output, "error": "", "success": True}
                except PermissionError:
                    return {"output": "", "error": "Error: Permission denied", "success": False}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "cd":
                try:
                    if not args:
                        # Go to home directory
                        home_dir = os.path.expanduser("~")
                        if self.is_safe_path(home_dir):
                            self.current_dir = home_dir
                            return {"output": "", "error": "", "success": True}
                        else:
                            return {"output": "", "error": "Error: Cannot access home directory", "success": False}
                    
                    target = args[0].strip('"\'')
                    
                    if target == "..":
                        parent = os.path.dirname(self.current_dir)
                        if parent and self.is_safe_path(parent):
                            self.current_dir = parent
                        else:
                            return {"output": "", "error": "Error: Cannot go up from this directory", "success": False}
                    elif target.startswith("/") or (len(target) > 1 and target[1] == ":"):
                        # Absolute path
                        if os.path.exists(target) and os.path.isdir(target) and self.is_safe_path(target):
                            self.current_dir = os.path.abspath(target)
                        else:
                            return {"output": "", "error": f"Error: Directory not found or access denied: {target}", "success": False}
                    else:
                        # Relative path
                        new_path = os.path.join(self.current_dir, target)
                        if os.path.exists(new_path) and os.path.isdir(new_path) and self.is_safe_path(new_path):
                            self.current_dir = os.path.abspath(new_path)
                        else:
                            return {"output": "", "error": f"Error: Directory not found or access denied: {target}", "success": False}
                    
                    return {"output": "", "error": "", "success": True}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "mkdir":
                try:
                    if not args:
                        return {"output": "", "error": "Error: Please specify a directory name.", "success": False}
                    
                    dir_name = args[0].strip('"\'')
                    new_path = os.path.join(self.current_dir, dir_name)
                    
                    if not self.is_safe_path(new_path):
                        return {"output": "", "error": "Error: Cannot create directory in this location", "success": False}
                    
                    os.makedirs(new_path, exist_ok=False)
                    return {"output": f"Directory '{dir_name}' created successfully.", "error": "", "success": True}
                except FileExistsError:
                    return {"output": "", "error": f"Error: Directory already exists: {args[0]}", "success": False}
                except PermissionError:
                    return {"output": "", "error": "Error: Permission denied - cannot create directory", "success": False}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "rm":
                try:
                    if not args:
                        return {"output": "", "error": "Error: Please specify a file or directory to remove.", "success": False}
                    
                    target = args[0].strip('"\'')
                    target_path = os.path.join(self.current_dir, target)
                    
                    if not self.is_safe_path(target_path):
                        return {"output": "", "error": "Error: Cannot remove files from this location", "success": False}
                    
                    if os.path.isfile(target_path):
                        os.remove(target_path)
                        return {"output": f"File '{target}' removed successfully.", "error": "", "success": True}
                    elif os.path.isdir(target_path):
                        shutil.rmtree(target_path)
                        return {"output": f"Directory '{target}' removed successfully.", "error": "", "success": True}
                    else:
                        return {"output": "", "error": f"Error: File or directory not found: {target}", "success": False}
                except PermissionError:
                    return {"output": "", "error": "Error: Permission denied - cannot remove file/directory", "success": False}
                except Exception as e:
                    return {"output": "", "error": f"Error: {str(e)}", "success": False}
            
            elif command == "history":
                if not self.history:
                    return {"output": "(no commands in history)", "error": "", "success": True}
                output = "\n".join([f"{i+1:>3}: {cmd}" for i, cmd in enumerate(self.history)])
                return {"output": output, "error": "", "success": True}
            
            elif command == "clear":
                return {"output": "CLEAR_TERMINAL", "error": "", "success": True}
            
            elif command == "help":
                help_text = """Available commands:
ls - List files and directories
cd <directory> - Change directory  
pwd - Show current directory
mkdir <name> - Create a directory
rm <path> - Remove file or directory
history - Show command history
clear - Clear terminal
help - Show this help message

You can also use natural language! Try:
- "show me what's in this directory"
- "create a folder called test"
- "go to the documents folder"
- "where am I right now?"
- "delete the temp folder"

⚠️  Security Note: Operations are restricted to safe directories for security."""
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
        user_sessions[session_id] = RealFileSystem()
    
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
                "prompt": user_fs.get_display_path()
            })
        
        # Try to interpret the command using natural language
        interpreted = interpret_command(user_input)
        final_command = interpreted if interpreted else user_input
        
        # Execute the command
        result = user_fs.execute_command(final_command)
        result["prompt"] = user_fs.get_display_path()
        
        # Show interpretation if it was used
        if interpreted and interpreted != user_input:
            result["interpretation"] = f"Interpreted as: {interpreted}"
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "output": "",
            "error": f"Server error: {str(e)}",
            "success": False,
            "prompt": os.getcwd()
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# For Vercel deployment
app = app
