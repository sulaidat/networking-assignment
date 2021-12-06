import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5566))
s.send(b'tuyendeptrai123')
print(s.recv(1024))