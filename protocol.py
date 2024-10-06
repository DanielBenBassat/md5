"""
prtocol has 3 type of messages:
request work: r ,len(num of cores), num of cores
receive work: j ,len(data) ,start ,end,  md5 target
finish work: f, len(num), num. 0 if not found, the target number if found
"""


def protocol_send(cmd, data):
    """
    function to send protocol message
    :param cmd: name of the command
    :param data: data according to cmd
    :return:
    """
    length = len(str(data))
    msg = str(cmd) + str(length) + "!" + str(data)
    return msg.encode()


def protocol_receive(my_socket):
    """
    receive protocol message
    :param my_socket: socket to receive from server
    :return: tuple of cmd and data
    """
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





