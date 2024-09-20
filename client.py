import socket
import hashlib
import os

IP = "127.0.0.1"
PORT = 5555


def calculate_md5(start, end, md5_target):
    for i in range(start, end + 1):
        num_str = str(i).zfill(3)
        md5_hash = hashlib.md5(num_str.encode()).hexdigest()
        if md5_hash == md5_target:
            return i
    return -1


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    num_cores = os.cpu_count()

    # Send num of cores to server
    client_socket.send(str(num_cores).encode())
    print(num_cores)


if __name__ == "__main__":
    main()
