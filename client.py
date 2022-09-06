import socket

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)

# STEP 1: send the hello message (message index = 0), receive the ack (message index = 1)

hello_msg = '0hello from client'.encode('utf-8')
buffer_size = 0

while True:
    s.sendto(hello_msg, (host, port))
    try:
        data = s.recv(1024)
    except socket.timeout:
        print('!time out for hello message!')
    else:
        data = data.decode('utf-8')
        if data[0] == '1':
            buffer_size = data[1:data.find(' ')]
            print(data[data.find(' ') + 1:])
            break

# STEP 2: send the file (message index = 2), receive the ack (message index = 3)

file = open('file1.txt', 'rb')
chunk_count = 0
while True:
    chunk = file.read(int(buffer_size))
    chunk_count += 1
    if not chunk:
        break
    while True:
        s.sendto(f'2{chunk_count} '.encode() + chunk, (host, port))
        try:
            data = s.recv(1024)
        except socket.timeout:
            print('!time out for file message!')
        else:
            data = data.decode('utf-8')
            if data[0] == '3' and data[1:data.find(' ')] == str(chunk_count):
                print(data[data.find(' ') + 1:], ' \"', chunk.decode(), '\"', sep='')
                break

# STEP 3: send the final message (message index = 4), receive the ack (message index = 5)

while True:
    s.sendto('4end of file'.encode(), (host, port))
    try:
        data = s.recv(1024)
    except socket.timeout:
        print('!time out for final message!')
    else:
        data = data.decode('utf-8')
        if data[0] == '5':
            print(data[1:])
            break

