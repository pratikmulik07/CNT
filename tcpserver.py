import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '0.0.0.0'
server_port = 12346

server_socket.bind((server_host, server_port))
server_socket.listen(1)

print(f"Server listening on {server_host}:{server_port}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected with {client_address}")

    while True:
        # Receive filename first
        filename = client_socket.recv(1024).decode()
        if filename.lower() == 'exit':
            print("Client has exited.")
            break

        save_path = os.path.join("received_" + filename)

        with open(save_path, "wb") as f:
            print(f"Receiving and saving as '{save_path}'...")
            while True:
                data = client_socket.recv(1024)
                if b"<<EOF>>" in data:
                    # Remove marker before writing last part
                    data = data.replace(b"<<EOF>>", b"")
                    f.write(data)
                    break
                f.write(data)

        print("✅ File received successfully.")

        # If client sends exit, break the loop to stop accepting new clients
        data = client_socket.recv(1024).decode()
        if data.lower() == 'exit':
            print("Client has exited.")
            break

    client_socket.close()
    print("Server is closing....")
    break
server_socket.close()
