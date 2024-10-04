import socket
import hashlib
import os
import protocol
import logging
import threading

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'

IP = "127.0.0.1"
PORT = 5555

lock = threading.Lock()
found = False


def calculate_md5(start, end, md5_target, client_socket):
    global found
    for i in range(start, end + 1):
        if found:
            return

        num_str = str(i).zfill(3)
        md5_hash = hashlib.md5(num_str.encode()).hexdigest()
        if md5_hash == md5_target:
            with lock:
                found = True
            client_socket.send(protocol.protocol_send("f", i))
            logging.debug("number is found: " + str(i))
            print(protocol.protocol_send("f", i))



def main():
    global found
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        num_cores = os.cpu_count()
        while not found:
            # Send num of cores to server
            client_socket.send(protocol.protocol_send("r", num_cores))
            print(protocol.protocol_send("r", num_cores))

            # receive work to do from server
            cmd, data = protocol.protocol_receive(client_socket)
            print("cmd: " + cmd + " data: " + " ".join(data))
            if cmd == 's':
                logging.debug("stop working")
                break

            start = int(data[0])
            end = int(data[1])
            target_md5 = data[2]
            step = (end - start) // num_cores
            threads = []
            for i in range(num_cores):
                range_start = start + i * step
                if i != num_cores - 1:
                    range_end = start + (i + 1) * step
                else:
                    range_end = end
                t = threading.Thread(target=calculate_md5, args=(range_start, range_end, target_md5, client_socket))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            if not found:
                client_socket.send(protocol.protocol_send("f", 0))
                print(protocol.protocol_send("f", 0))

    except socket.error:
        logging.debug(f"[ERROR] Connection with lost.")

    finally:
        logging.debug("close connection")
        client_socket.close()



if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
