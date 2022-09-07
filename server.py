import socket
import threading
import time

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
s.bind(("", port))

clients = {}
chunk_size = 2


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
        if client_msg[0] == '0':
            if client_address not in clients.keys():
                clients[client_address] = []
                clients[client_address].append('message 0 was received')
                print(client_msg[1:])
            reply = f'1{chunk_size} server received the hello message'.encode('utf-8')
            s.sendto(reply, client_address)
        elif client_msg[0] == '2':
            if len(clients[client_address]) == 0:
                print(f'the session of client {client_address} is closed')
                continue
            if len(clients[client_address]) == 1:
                clients[client_address].append('')
            if client_msg[1] == '0':
                clients[client_address].append(open(client_msg[3:], 'wb'))
                clients[client_address][1] += '0'
            chunk_index = client_msg.find(' ')
            if clients[client_address][1][-1] != client_msg[1:chunk_index] or len(clients[client_address][1]) == 0:
                clients[client_address][1] += client_msg[1:chunk_index]
                clients[client_address][2].write(client_msg[chunk_index + 1:].encode())
            reply = f'3{client_msg[1]} server received the chunk'.encode('utf-8')
            print(f'chunk {client_msg[1:chunk_index]} is received')
            s.sendto(reply, client_address)
        elif client_msg[0] == '4':
            if len(clients[client_address]) == 0:
                print(f'the session of client {client_address} is closed')
                continue
            reply = '5server received the file'.encode('utf-8')
            s.sendto(reply, client_address)
            print('data transfer is finished')
            timer.file_transfer_is_finished()
        timer = Timer(client_address)
        timer.start()


