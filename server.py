#!/usr/bin/env python3
# server.py

from posixpath import expanduser
import socket
from selectors import EVENT_READ, EVENT_WRITE
from util.loop import Loop
from util.currency import *
from util.timer import MyThread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5566))
s.listen(10240)
s.setblocking(False)

loop = Loop()

man_shell = """
Dac Cong's Currency Interactive Shell

Commands:
    help        print this manual
    latest      request the most recent exchange rate data (base: EUR)
    historical  request historical rates for a specific day (base: EUR)
    convert     convert any amount from one currency to another using real-time exchange rates

Run <command> -h for more information
"""

man_latest = """
latest - Request the most recent exchange rate data (base: EUR)

Usage:  
    latest -h                   help
    latest                      return all symbols
    latest [<list of symbols>]  return specified symbols
"""

man_historical = """
historical - Request historical rates for a specific day (base: EUR)

Usage:
    historical -h                       help
    historical <date>                   return all symbols
    historical <date> <list of symbols> return specified symbols
"""

man_convert = """
convert - Convert any amount from one currency to another

Usage:
    convert -h                       help
    convert                   return all symbols
    convert <date> <list of symbols> return specified symbols
"""

def interpret(msg):
    if not msg:
        return man_shell

    msg = msg.split()
    if msg[0] == 'latest':
        try:
            data = latest(msg[1:])
            msg = json.dumps(data)
        except KeyError:
            msg = man_latest
    elif msg[0] == 'historical':
        try:
            data = historical(msg[1], msg[2:])
            msg = json.dumps(data)
        except (KeyError, IndexError):
            msg = man_historical
    elif msg[0] == 'convert':
        try:
            msg = str(convert(msg[1], msg[2], msg[3], msg[4]))
        except IndexError:
            try:
                msg = str(convert(msg[1], msg[2], msg[3]))
            except (KeyError, IndexError):
                msg = man_convert
    else:
        msg = man_shell
    return msg

def handler(conn):
    while True:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        msg = interpret(msg.decode()).encode()
        yield from loop.send(conn, msg)

def main():
    while True:
        conn, addr = yield from loop.accept(s)
        conn.setblocking(False)
        loop.create_task((handler(conn), None))

thread = MyThread(10)   # update every 10 seconds
thread.start()
loop.create_task((main(), None))
loop.run()
