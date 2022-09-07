import os.path
import socket
import threading
import time

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
s.bind(("", port))

clients = {}
buf_size = 2


class Timer(threading.Thread):
    def __init__(self, client_addr):
        super().__init__()
        self.client_address = client_addr
        self.time_to_close_session = False

    def run(self):
        super().run()
        time.sleep(3)
        self.time_to_close_session = True

    @staticmethod
    def file_transfer_is_finished():
        time.sleep(1)
        clients.pop(client_address)

    def try_to_close_session(self):
        if self.time_to_close_session:
            clients.pop(client_address)


got_first_message = False
while True:
    try:
        client_msg, client_address = s.recvfrom(1024)
    except socket.timeout:
        print('!time out: waiting for a new message!')
    else:
        if got_first_message:
            timer.try_to_close_session()
        else:
            got_first_message = True
        client_msg = client_msg.decode('utf-8')

        if client_msg[0] == 's':
            if client_address not in clients.keys():
                clients[client_address] = []
                clients[client_address].append(client_msg.split(' ')[2])  # filename
                clients[client_address].append(client_msg.split(' ')[3])  # size
                print('hello from client:', client_msg)
            reply = f'1{buf_size} server received the hello message'.encode('utf-8')
            s.sendto(reply, client_address)

        elif client_msg[0] == 'd':
            if client_address not in clients.keys():
                print(f'the session of client {client_address} is closed')
                continue
            if len(clients[client_address]) == 2:
                clients[client_address].append('')  # seq_no checker
                clients[client_address].append(open(clients[client_address][0], 'wb'))  # new file
                clients[client_address].append(int(clients[client_address][1]) / buf_size + 1)
            chunk_index = client_msg.find(' ') + 1

            if clients[client_address][2] != client_msg[1:chunk_index - 1]:
                clients[client_address][2] = client_msg[1:chunk_index - 1]
                clients[client_address][3].write(client_msg[chunk_index:].encode())
            reply = f'3{client_msg[1:chunk_index - 1]} server received the chunk'.encode('utf-8')
            print(f'chunk {client_msg[1:chunk_index - 1]} is received')
            s.sendto(reply, client_address)

            if int(clients[client_address][2]) >= clients[client_address][4]:
                print('data transfer is finished')
                clients[client_address][3].close()
                timer.file_transfer_is_finished()

        timer = Timer(client_address)
        timer.start()


