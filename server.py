import socket
import threading

IP = "127.0.0.1"
PORT = 5555


def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message != "exit":
                print(f"[{address}] {message}")
                # Echo the message back to the client
                client_socket.send(f"Echo: {message}".encode())
            else:
                break
        except socket.error:
            print(f"[ERROR] Connection with {address} lost.")
            break

    client_socket.close()
    print(f"[DISCONNECT] {address} has disconnected.")



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
