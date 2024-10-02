import socket
import threading

import protocol

import logging

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


IP = "127.0.0.1"
PORT = 5555
CLIENTS_SOCKETS = []
threads = []
MD5_TARGET = "0a571f99e5667cb088dadcc9a2d1e161"
NUM_PER_CORE = 10
lock = threading.Lock()
task_start = 0
found = False




def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    global task_start, found, CLIENTS_SOCKETS
    try:
        while not found:
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
            result = int(data[0])
            print(result)
            if result != 0:
                found = True
                for client_socket in CLIENTS_SOCKETS:
                    client_socket.sendall(protocol.protocol_send("s", ""))









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
        threads.append(thread)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
