import socket

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
s.bind(("", port))

clients = {}
chunk_size = 2

while True:
    try:
        client_msg, client_address = s.recvfrom(1024)
    except socket.timeout:
        print('!time out: waiting for a new message!')
    else:
        client_msg = client_msg.decode('utf-8')
        if client_msg[0] == '0':
            if client_address not in clients.keys():
                clients[client_address] = []
                clients[client_address].append('message 0 was received')
                print(client_msg[1:])
            reply = f'1{chunk_size} server received the hello message'.encode('utf-8')
            s.sendto(reply, client_address)
        elif client_msg[0] == '2':
            if len(clients[client_address]) == 1:
                clients[client_address].append('')
            chunk = client_msg[client_msg.find(' ') + 1:]
            if len(clients[client_address][1]) < chunk_size * int(client_msg[1:client_msg.find(' ')]):
                clients[client_address][1] += chunk
            reply = f'3{client_msg[1]} server received the chunk'.encode('utf-8')
            print(f'chunk \"{chunk}\" is received')
            s.sendto(reply, client_address)
        elif client_msg[0] == '4':
            reply = '5server received the file'.encode('utf-8')
            s.sendto(reply, client_address)
            print('file:', clients[client_address][1])
            print('data transfer is finished')
            clients.pop(client_address)
