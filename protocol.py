
def protocol_send(cmd, data):
    length = len(str(data))
    msg = str(cmd) + str(length) + "!" + str(data)
    return msg.encode()


def protocol_receive(my_socket):
    cmd = my_socket.recv(1).decode()
    data_len = ""
    cur_char = my_socket.recv(1).decode()
    while cur_char != '!':
        data_len += cur_char
        cur_char = my_socket.recv(1).decode()
    data_len = int(data_len)
    data = ""
    for i in range(data_len):
        data += my_socket.recv(1).decode()

    data_list = data.split("!")


    return cmd, data_list





