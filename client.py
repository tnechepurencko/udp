import os.path
import socket
import sys

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timeout = 0.5
s.settimeout(timeout)

# STEP 1: send the hello message (message index = 0), receive the ack (message index = 1)

filename = 'theFile'
file = open('file1.txt', 'rb')
hello_msg = f's 0 {filename} {os.path.getsize(file.name)}'.encode('utf-8')
buffer_size = 0

send_count = 0
while True:
    send_count += 1
    if send_count >= 5:
        sys.exit(1)
    s.sendto(hello_msg, (host, port))
    try:
        data = s.recv(1024)
    except socket.timeout:
        print('!time out for hello message!')
    else:
        data = data.decode('utf-8')
        if data[0] == '1':
            buffer_size = int(data[1:data.find(' ')])
            print(data[data.find(' ') + 1:])
            break

# STEP 2: send the file (message index = 2), receive the ack (message index = 3)

seq_no = 1
while True:
    chunk = file.read(buffer_size)
    seq_no += 1
    if not chunk:
        break
    send_count = 0
    while True:
        send_count += 1
        if send_count >= 5:
            sys.exit(1)
        s.sendto(f'd{seq_no} '.encode() + chunk, (host, port))
        try:
            data = s.recv(1024)
        except socket.timeout:
            print('!time out for file message!')
        else:
            data = data.decode('utf-8')
            if data[0] == '3' and data[1:data.find(' ')] == str(seq_no):
                print(data[data.find(' ') + 1:], seq_no)
                break


