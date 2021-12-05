#!/usr/bin/env python3
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5566))

while True:
    msg = input("$ ")
    s.send(msg.encode())
    msg = s.recv(4096).decode()
    print(msg)
