import socket

IP = "127.0.0.1"
PORT = 5555


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    while True:
        message = input("You: ")

        # Send message to server
        client_socket.send(message.encode())
        # Receive echo from the server
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")

    client_socket.close()


if __name__ == "__main__":
    main()
