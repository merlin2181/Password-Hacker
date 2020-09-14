import argparse
import socket

pass_hacker = argparse.ArgumentParser(description='An automated password hacker')
pass_hacker.add_argument("hostname", type=str, help='the IP address or domain name of the site you are trying to hack')
pass_hacker.add_argument("port", type=int, help='the port number of the site you are trying to hack')
pass_hacker.add_argument("message", type=str, help='the data you want to send to the site')
args = pass_hacker.parse_args()

hacker = socket.socket()
address = (args.hostname, args.port)
with hacker as h:
    data = args.message.encode()
    h.connect(address)
    h.send(data)
    rec_data = h.recv(1024)
    print(rec_data.decode())
