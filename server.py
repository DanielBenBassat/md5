import socket
import threading

import protocol

IP = "127.0.0.1"
PORT = 5555
CLIENTS_SOCKETS = []
MD5_TARGET = 'f899139df5e1059396431415e770c6dd'
NUM_PER_CORE = 5
lock = threading.Lock()
task_start = 0




def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    global task_start
    try:
        # receive num of cores
        cmd, data = protocol.protocol_receive(client_socket)
        print(cmd)
        print(data)

        # send work frame
        lock.acquire()
        start = task_start
        end = start + int(data[0]) * NUM_PER_CORE - 1
        data = str(start) + "!" + str(end) + "!" + MD5_TARGET
        client_socket.send(protocol.protocol_send("j", data))
        print(protocol.protocol_send("j", data))
        task_start = end + 1
        lock.release()

        # receive if found
        cmd, data = protocol.protocol_receive(client_socket)
        print(cmd)
        print(data)




    except socket.error:
        print(f"[ERROR] Connection with {address} lost.")

    finally:
        client_socket.close()
        print(f"[DISCONNECT] {address} has disconnected.")



def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        CLIENTS_SOCKETS.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
