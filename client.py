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

stop_flag = False


def calculate_md5(start, end, md5_target, index):
    global stop_flag, result_list
    for i in range(start, end + 1):
        if stop_flag:
            return

        num_str = str(i).zfill(3)
        md5_hash = hashlib.md5(num_str.encode()).hexdigest()
        if md5_hash == md5_target:
            stop_flag = True
            return i
    return 0


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        num_cores = os.cpu_count()
        while True:
            # Send num of cores to server
            client_socket.send(protocol.protocol_send("r", num_cores))
            #print(protocol.protocol_send("r", num_cores))

            # receive work to do from server
            cmd, data = protocol.protocol_receive(client_socket)
            #print("cmd: " + cmd + " data: " + " ".join(data))
            if cmd == 's':
                logging.debug("stop working")
                break

            start = int(data[0])
            end = int(data[1])
            target_md5 = data[2]
            step = (end - start) // num_cores
            threads = []
            result_list = []
            for i in range(num_cores):
                range_start = start + i * step
                if i != num_cores - 1:
                    range_end = start + (i + 1) * step
                else:
                    range_end = end

                t = threading.Thread(target=calculate_md5(), args=(range_start, range_end, target_md5, i))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            #target_num = calculate_md5(int(data[0]), int(data[1]), data[2])
            #print(target_num)
            #if target_num != 0:
              #  logging.debug("number is found: " + str(target_num))

            # send if found to server
            client_socket.send(protocol.protocol_send("f", target_num))
            #print(protocol.protocol_send("f", target_num))

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
