#!/usr/bin/env python3
# echoserver.py

import socket
from selectors import EVENT_READ, EVENT_WRITE
from util.loop import Loop

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5566))
s.listen(10240)
s.setblocking(False)

loop = Loop()

def handler(conn):
    """
    - If run normal then continue until we got data from callee, or msg=None.
    - If msg=None (connection is down) then break and raise StopIteration
    - If we got data from callee then send it back to caller
    """
    while True:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        yield from loop.send(conn, msg)

def main():
    """
    - If there's an accepted connection then create new task to manipulate
    - If we got data from callee then send it back to caller
    """
    while True:
        conn, addr = yield from loop.accept(s)
        conn.setblocking(False)
        loop.create_task((handler(conn), None))

loop.create_task((main(), None))
loop.run()