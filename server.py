#!/usr/bin/env python3
# server.py

import socket
# import fcntl
# import sys
from urllib.error import HTTPError
from util.loop_window import Loop
from util.currency import *
from util.user import *
from util.timer import TimerThread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5566))
s.listen(10240)
s.setblocking(False)

# set sys.stdin non-blocking
# orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
# fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

loop = Loop()

MAN_SHELL = """
Dac Cong's Currency Interactive Shell

Commands:
    help        print this manual`
    latest      request the most recent exchange rate data (base: EUR)
    historical  request historical rates for a specific day (base: EUR)
    convert     convert any amount from one currency to another using real-time exchange rates

Run <command> -h for more information
"""

MAN_LATEST = """
latest - Request the most recent exchange rate data (base: EUR)

Usage:  
    latest -h                   help
    latest                      return all symbols
    latest [<list of symbols>]  return specified symbols
"""

MAN_HISTORICAL = """
historical - Request historical rates for a specific day (base: EUR)

Usage:
    historical -h                       help
    historical <date>                   return all symbols
    historical <date> <list of symbols> return specified symbols
    date format is YYYY-MM-DD
"""

MAN_CONVERT = """
convert - Convert any amount from one currency to another

Usage:
    convert -h                       help
    convert                   return all symbols
    convert <date> <list of symbols> return specified symbols
"""

MAN_LOGIN = """
login - login

Usage:
    login <username> <password>
"""

MAN_REGISTER = """
register - register account

Usage:
    register <username> <password>
"""

def interpret(msg):
    if not msg:
        return MAN_SHELL

    msg = msg.split()
    if msg[0] == 'latest':
        try:
            data = latest(msg[1:])
            msg = json.dumps(data)
        except KeyError:
            msg = MAN_LATEST
    elif msg[0] == 'historical':
        try:
            data = historical(msg[1], msg[2:])
            msg = json.dumps(data)
        except (KeyError, IndexError, HTTPError):
            msg = MAN_HISTORICAL
    elif msg[0] == 'convert':
        try:
            msg = str(convert(msg[1], msg[2], msg[3], msg[4]))
        except IndexError:
            try:
                msg = str(convert(msg[1], msg[2], msg[3]))
            except (KeyError, IndexError):
                msg = MAN_CONVERT
    else:
        msg = MAN_SHELL
    return msg

def interpret_before_handler(msg):
    if not msg:
        return MAN_LOGIN

    msg = msg.split()
    if msg[0] == 'register':
        try:
            msg = register(msg[1], msg[2])
            if msg:
                msg = 'Account successfully registered'
            else:
                msg = 'Account already exists'
        except IndexError:
            msg = MAN_REGISTER   
    elif msg[0] == 'login':
        try:
            msg = login(msg[1], msg[2])
            if msg:
                msg = 'True'   # success
            else:
                msg = 'Username or password incorrect!'    
        except IndexError:
            msg = MAN_LOGIN    # wrong syntax
    elif msg[0] == 'quit':
        msg = 'Quitted'
    else:
        msg = 'You must login first!'
    return msg

def handler(conn):
    while True:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        msg = interpret(msg.decode()).encode()
        yield from loop.send(conn, msg)

def before_handler(conn):
    logged = False
    while not logged:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        msg = interpret_before_handler(msg.decode())
        if msg == 'Quitted':
            yield from loop.send(conn, msg.encode())
            conn.close()
            break
        elif msg == 'True':
            msg = 'Logged in successfully'
            loop.create_task((handler(conn), None))
            logged = True
        msg = msg.encode()
        yield from loop.send(conn, msg)



def main():
    while True:
        conn, addr = yield from loop.accept(s)
        conn.setblocking(False)
        loop.create_task((before_handler(conn), None))

thread = TimerThread(1800)   # update every 30 minutes
thread.start()
loop.create_task((main(), None))
loop.run()
