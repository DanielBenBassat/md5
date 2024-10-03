import socket
import hashlib
import os
import protocol
import logging

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'

IP = "127.0.0.1"
PORT = 5555


def calculate_md5(start, end, md5_target):
    for i in range(start, end + 1):
        num_str = str(i).zfill(3)
        md5_hash = hashlib.md5(num_str.encode()).hexdigest()
        if md5_hash == md5_target:
            return i
    return 0


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    num_cores = os.cpu_count()
    while True:
        # Send num of cores to server
        client_socket.send(protocol.protocol_send("r", num_cores))
        print(protocol.protocol_send("r", num_cores))

        # receive work to do from server
        cmd, data = protocol.protocol_receive(client_socket)
        if cmd == 's':
            break
        print(cmd)
        print(data)

        target_num = calculate_md5(int(data[0]), int(data[1]), data[2])
        print(target_num)

        # send if found to server
        client_socket.send(protocol.protocol_send("f", target_num))
        print(protocol.protocol_send("f", target_num))

    print("i was told to be clodes")
    client_socket.close()




if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
