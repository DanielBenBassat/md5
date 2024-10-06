import socket
import threading
import protocol
import logging
import os

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


IP = "127.0.0.1"
PORT = 5555
CLIENTS_SOCKETS = []
threads = []
MD5_TARGET = "25f9e794323b453885f5181f1b624d0b"
NUM_PER_CORE = 10000
lock = threading.Lock()
task_start = 0
found = False


def handle_client(client_socket, address):
    """
    the function for each client of socket. gives work for clients and receive if found or not. if found tells all client stop working and if not continue to give work
    :param client_socket: client socket
    :param address: ip and port of client
    :return:
    """
    logging.debug(f"[NEW CONNECTION] {address} connected.")
    global task_start, found, CLIENTS_SOCKETS
    try:
        while not found:
            # receive num of cores
            cmd, data = protocol.protocol_receive(client_socket)
            # send work frame
            lock.acquire()
            start = task_start
            end = start + int(data[0]) * NUM_PER_CORE - 1
            data = str(start) + "!" + str(end) + "!" + MD5_TARGET
            client_socket.send(protocol.protocol_send("j", data))
            task_start = end + 1
            lock.release()

            # receive if found or not
            cmd, data = protocol.protocol_receive(client_socket)

            result = int(data[0])
            if result != 0:
                logging.debug("result is " + str(result))
                with lock:
                    found = True
                for client_socket in CLIENTS_SOCKETS:
                    client_socket.send(protocol.protocol_send("s", ""))

    except socket.error:
        logging.debug(f"[ERROR] Connection with {address} lost.")


def main():
    """
    server accept client and close connection when found is true
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((IP, PORT))
        server.listen()
        logging.debug("********************************************************")
        logging.debug(f"[LISTENING] Server is listening on {IP}:{PORT}")

        global found
        server.settimeout(0.5)
        while not found:
            try:
                client_socket, client_address = server.accept()
                CLIENTS_SOCKETS.append(client_socket)
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                threads.append(thread)
                thread.start()
                logging.debug(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            except socket.timeout:
                pass
    except socket.error:
        logging.debug("socket error")
    finally:
        server.close()
        logging.debug("server is closed")


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
