import socket
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '127.0.0.1'
server_port = 12346

client_socket.connect((server_host, server_port))
print(f"Connected to {server_host}:{server_port}")

while True:
    file_path = input("Enter full path of the file to send (or type 'exit' to quit): ")

    if file_path.lower() == 'exit':
        print("You chose to exit.")
        client_socket.send(b"<<EXIT>>")
        break

    if not os.path.exists(file_path):
        print("File does not exist.")
        continue

    filename = os.path.basename(file_path)
    client_socket.send(filename.encode())

    with open(file_path, "rb") as f:
        print(f"Sending '{filename}'...")
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.send(data)

    # Send end marker
    client_socket.send(b"<<EOF>>")
    print("File sent successfully.")

client_socket.close()
