import os
import shutil
import subprocess
import sys
import re

import re

import re

def interpret_command(query):
    raw_query = query.strip()
    query = raw_query.lower()
    words = query.split()

    # --- Helper: extract quoted or named target ---
    target = ""
    match = re.search(r'["\']([^"\']+)["\']', raw_query)  # preserve case inside quotes
    if match:
        target = match.group(1)
    else:
        skip_words = {"the", "a", "an", "called", "named"}
        for i, w in enumerate(words):
            if w in ["folder", "directory", "file", "into", "to"]:
                if i + 1 < len(words):
                    nxt = raw_query.split()[i + 1]  # preserve case
                    if nxt.lower() not in skip_words:
                        target = nxt
                        break
        if not target and len(words) > 1:
            last = raw_query.split()[-1]
            if last.lower() not in skip_words:
                target = last

    # clean target
    target = target.strip("\"'")

    # wrap multi-word names in quotes
    if " " in target:
        target = f"\"{target}\""

    # --- ls command ---
    if any(phrase in query for phrase in ["show me", "list", "what's in", "whats in", "see files", "ls", "there?"]):
        if not any(w in words for w in ["create", "make", "delete", "remove", "go", "cd", "where"]):
            return "ls"

    # --- pwd command ---
    if any(phrase in query for phrase in [
        "where am i", "current directory", "pwd", "current path",
        "where am i right now", "show me the current path"
    ]):
        return "pwd"

    # --- mkdir command ---
    if any(w in words for w in ["create", "make"]):
        if "folder" in words or "directory" in words:
            return f'mkdir {target}'
        if len(words) > 1 and words[0] in ["create", "make"]:
            return f'mkdir {target}'

    # --- rm command ---
    if any(w in words for w in ["delete", "remove", "rm"]):
        if target:
            return f'rm {target}'

    # --- cd command ---
    if any(w in words for w in ["go", "navigate", "cd", "enter", "change"]):
        if "directory" in words or "folder" in words or "into" in words or "to" in words:
            return f'cd {target}'
        if len(words) > 1 and words[0] in ["go", "cd", "enter"]:
            return f'cd {target}'

    return ""  # no match

    query = query.lower().strip()
    words = query.split()

    # --- Helper: extract quoted or named target ---
    target = ""
    match = re.search(r'["\']([^"\']+)["\']', query)
    if match:
        target = match.group(1)  # use the content inside quotes
    else:
        # pick word after folder/directory/file/named
        for key in ["folder", "directory", "file", "named", "into", "to"]:
            if key in words:
                idx = words.index(key)
                if idx + 1 < len(words):
                    target = words[idx + 1]
                    break
        # fallback: last word
        if not target and len(words) > 1:
            target = words[-1]

    # clean up target (remove quotes if any remain)
    target = target.strip("\"'")

    # --- ls command ---
    if any(phrase in query for phrase in ["show me", "list", "what's in", "whats in", "see files", "ls", "there?"]):
        if not any(w in words for w in ["create", "make", "delete", "remove", "go", "cd", "where"]):
            return "ls"

    # --- pwd command ---
    if any(phrase in query for phrase in ["where am i", "current directory", "pwd", "current path", "where am i right now", "show me the current path"]):
        return "pwd"

    # --- mkdir command ---
    if any(w in words for w in ["create", "make"]):
        if "folder" in words or "directory" in words:
            return f'mkdir {target}'
        if len(words) > 1 and words[0] in ["create", "make"]:
            return f'mkdir {target}'

    # --- rm command ---
    if any(w in words for w in ["delete", "remove", "rm"]):
        if target:
            return f'rm {target}'

    # --- cd command ---
    if any(w in words for w in ["go", "navigate", "cd", "enter", "change"]):
        if "directory" in words or "folder" in words or "into" in words or "to" in words:
            return f'cd {target}'
        if len(words) > 1 and words[0] in ["go", "cd", "enter"]:
            return f'cd {target}'

    return ""  # no match

    query = query.lower().strip()
    words = query.split()

    # --- Helper: extract quoted or named target ---
    match = re.search(r'["\']([^"\']+)["\']', query)
    if match:
        target = match.group(1)  # use quoted name
    else:
        # try after keywords
        for key in ["folder", "directory", "file", "named", "into", "to"]:
            if key in words:
                idx = words.index(key)
                if idx + 1 < len(words):
                    target = words[idx + 1]
                    break
        else:
            target = words[-1] if len(words) > 1 else ""

    # --- ls command ---
    if any(phrase in query for phrase in ["show me", "list", "what's in", "whats in", "see files", "ls", "there?"]):
        if not any(w in words for w in ["create", "make", "delete", "remove", "go", "cd", "where"]):
            return "ls"

    # --- pwd command ---
    if any(phrase in query for phrase in ["where am i", "current directory", "pwd", "current path", "where am i right now", "show me the current path"]):
        return "pwd"

    # --- mkdir command ---
    if any(w in words for w in ["create", "make"]):
        if "folder" in words or "directory" in words:
            return f'mkdir "{target}"'
        if len(words) > 1 and words[0] in ["create", "make"]:
            return f'mkdir "{target}"'

    # --- rm command ---
    if any(w in words for w in ["delete", "remove", "rm"]):
        if target:
            return f'rm "{target}"'

    # --- cd command ---
    if any(w in words for w in ["go", "navigate", "cd", "enter", "change"]):
        if "directory" in words or "folder" in words or "into" in words or "to" in words:
            return f'cd "{target}"'
        if len(words) > 1 and words[0] in ["go", "cd", "enter"]:
            return f'cd "{target}"'

    return ""  # no match
    query = query.lower().strip()
    words = query.split()
    
    # ls command
    if any(phrase in query for phrase in ["show me", "list", "what's in", "see files", "ls"]):
        if not any(word in words for word in ["create", "make", "delete", "remove", "go", "cd", "where"]):
            return "ls"

    # pwd command
    if any(phrase in query for phrase in ["where am i", "current directory", "pwd", "current path"]):
        return "pwd"

    # mkdir command
    if any(word in words for word in ["create", "make"]):
        if "folder" in words or "directory" in words:
            folder = words[-1].strip("\"'")
            return f"mkdir {folder}"
        if len(words) > 1 and words[0] in ["create", "make"]:
            folder = words[1].strip("\"'")
            return f"mkdir {folder}"

    # rm command
    if any(word in words for word in ["delete", "remove", "rm"]):
        if len(words) > 1:
            target = words[-1].strip("\"'")
            return f"rm {target}"

    # cd command
    if any(word in words for word in ["go", "navigate", "cd", "enter", "change"]):
        if "directory" in words or "folder" in words or "into" in words or "to" in words:
            target = words[-1].strip("\"'")
            return f"cd {target}"
        if len(words) > 1 and words[0] in ["go", "cd", "enter"]:
            target = words[1].strip("\"'")
            return f"cd {target}"

    return ""  # Return empty if no clear command is found

def main():
    command_history = []
    while True:
        prompt = f"PyTerm:{os.getcwd()} $ "
        command_input = input(prompt)
        
        if not command_input:
            continue
        
        command_history.append(command_input)
        
        interpreted_command = interpret_command(command_input)
        final_command_str = interpreted_command if interpreted_command else command_input
        
        parts = final_command_str.split()
        command = parts[0]
        args = parts[1:]
        
        if command == "exit":
            print("Exiting PyTerm. Goodbye!")
            sys.stdout.flush()
            break
        elif command == "history":
            for i, cmd in enumerate(command_history, 1):
                print(f"{i: >3}: {cmd}")
            sys.stdout.flush()
        elif command == "pwd":
            print(os.getcwd())
            sys.stdout.flush()
        elif command == "ls":
            try:
                items = os.listdir('.')
                for item in items:
                    print(item)
            except Exception as e:
                print(f"Error: {e}")
            sys.stdout.flush()
        elif command == "cd":
            try:
                if not args:
                    os.chdir(os.path.expanduser('~'))
                else:
                    os.chdir(args[0])
            except FileNotFoundError:
                print(f"Error: Directory not found: {args[0]}")
                sys.stdout.flush()
            except Exception as e:
                print(f"Error: {e}")
                sys.stdout.flush()
        elif command == "mkdir":
            try:
                os.mkdir(args[0])
                print(f"Directory '{args[0]}' created.")
            except IndexError:
                print("Error: Please specify a directory name.")
            except FileExistsError:
                print(f"Error: Directory already exists: {args[0]}")
            except Exception as e:
                print(f"Error: {e}")
            sys.stdout.flush()
        elif command == "rm":
            try:
                path_to_remove = args[0]
                if os.path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                    print(f"File '{path_to_remove}' removed.")
                elif os.path.isdir(path_to_remove):
                    shutil.rmtree(path_to_remove)
                    print(f"Directory '{path_to_remove}' removed.")
                else:
                    print(f"Error: File or directory not found: {path_to_remove}")
            except IndexError:
                print("Error: Please specify a file or directory to remove.")
            except Exception as e:
                print(f"Error: {e}")
            sys.stdout.flush()
        elif command == "sysinfo":
            try:
                print("--- System Information (Windows) ---")
                cpu_command = "powershell \"Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage\""
                cpu_result = subprocess.run(cpu_command, shell=True, capture_output=True, text=True)
                if cpu_result.returncode == 0 and cpu_result.stdout.strip():
                    print(f"CPU Usage: {cpu_result.stdout.strip()}%")
                else:
                    print("CPU Usage: Could not retrieve.")
                mem_command = "powershell \"$mem = Get-CimInstance Win32_OperatingSystem; [math]::Round((($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize) * 100, 2)\""
                mem_result = subprocess.run(mem_command, shell=True, capture_output=True, text=True)
                if mem_result.returncode == 0 and mem_result.stdout.strip():
                     print(f"Memory Usage: {mem_result.stdout.strip()}%")
                else:
                    print("Memory Usage: Could not retrieve.")
            except Exception as e:
                print(f"Error: Could not fetch system info using PowerShell.")
            sys.stdout.flush()
        else:
            print(f"Error: Command '{command}' not found.")
            sys.stdout.flush()

if __name__ == "__main__":
    main()