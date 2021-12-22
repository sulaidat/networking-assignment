#!/usr/bin/env python3
# server.py

import socket
import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from urllib.error import HTTPError
from util.loop import Loop
from util.currency import *
from util.user import *
from util.timer import TimerThread


Live_Account=[]
ID=[]
Ad=[]
LARGE_FONT = ("Bangers", 13, "bold")

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("PRO GUI")
        self.geometry("500x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=True, height=True)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
 
        self.frames = {}
        frame = ServerFrame(container, self)
        self.frames['serverFrame'] = frame 
        frame.grid(row=0, column=0, sticky="nsew")

        # self.showFrame('serverFrame')
    
    # def showFrame(self, container):
        
    #     frame = self.frames[container]
    #     if container==HomePage:
    #         self.geometry("500x350")
    #     else:
    #         self.geometry("500x150")
    #     frame.tkraise()
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

class ServerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="RoyalBlue4")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1], weight=1)

        lbl_Title = tk.Label(self, text="SERVER LOG", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        lbl_Title.grid(row=0, column=0)
        
        global txt_Logging_Box
        txt_Logging_Box = tk.Text(self, width=60, borderwidth=3, relief=tk.SUNKEN, bg="white")
        txt_Logging_Box.grid(row=1, column=0, sticky="nsew")
        txt_Logging_Box.config(state=DISABLED)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=txt_Logging_Box.yview)
        scrollbar.grid(row=1, column=1, sticky='news')
        txt_Logging_Box['yscrollcommand'] = scrollbar.set
        # Table.configure(yscroll=scrollbar.set)
        # scrollbar.grid(row=1, column=1, sticky='E')

        btn_end = tk.Button(self, text="END",bg="RoyalBlue4",fg='floral white')
        btn_end.grid(row= 2, column=1)

 
    def logging(msg):
        txt_Logging_Box.config(state=NORMAL)
        txt_Logging_Box.insert(tk.END, msg)
        txt_Logging_Box.config(state=DISABLED)

 
    # def UpdateStatus(msg):
    #     newClient = [address , Activate]
    #     Table.insert('', tk.END, values=newClient)

        # Table.configure("Treeview", background="#383838", foreground="white", fieldbackground="red")
            # close-programe function


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5566))
s.listen(10240)
s.setblocking(False)

loop = Loop()

MAN_SHELL = """
Dac Cong's Currency Interactive Shell

Commands:
    help        print this manual`
    latest      request the most recent exchange rate data (base: EUR)
    historical  request historical rates for a specific day (base: EUR)
    convert     convert any amount from one currency to another using real-time exchange rates
    timeseries  request exchange rates for a specific period of time
    login       login an account
    logout      logout
    register    register an account


Run <command> -h for more information
"""

MAN_LATEST = """
latest - Request the most recent exchange rate data (base: EUR)

Usage:  
    latest -h                   help
    latest                      return all symbols
    latest [<list of symbols>]  return specified symbols
Return: 
    json-like string data
"""

MAN_HISTORICAL = """
historical - Request historical rates for a specific day (base: EUR)

Usage:
    historical -h                       help
    historical <date>                   return all symbols
    historical <date> <list of symbols> return specified symbols
    date format is YYYY-MM-DD
Return:
    json-like string data
"""

MAN_CONVERT = """
convert - Convert any amount from one currency to another

Usage:
    convert -h                          help
    convert                             return all symbols
    convert <date> <list of symbols>    return specified symbols
Return:
    json-like string data
"""

MAN_TIMESERIES = """
timeseries - request exchange rates for a specific period of time

Usage:
    timeseries -h       help
    timeseries <start date> <end date> <base>   
                        return all symbols
    timeseries <start date> <end date> <base> <list of symbols> 
                        return specified symbols
Return:
    json-like string data
"""

MAN_LOGIN = """
login - login

Usage:
    login <username> <password>
Return:
    if success: return string "Logged in successfully"
    if account incorrect: return string "Username or password incorrect!"
"""

MAN_REGISTER = """
register - register account

Usage:
    register <username> <password>
Return:
    if account exists: return string "Account already exists"
    if success: return string "Account successfully registered"
"""

MAN_QUIT = """
quit

Usage: 
    quit
Return:
    string "Quitted"
"""


def interpret(msg, addr):
    if not msg:
        return MAN_SHELL

    msg = msg.split()

    if msg[0] == 'latest':
        try:
            data = latest(msg[1:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
        except KeyError:
            msg = MAN_LATEST

    elif msg[0] == 'historical':
        try:
            data = historical(msg[1], msg[2:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
        except (KeyError, IndexError, HTTPError):
            msg = MAN_HISTORICAL

    elif msg[0] == 'convert':
        try:
            msg = str(convert(msg[1], msg[2], msg[3], msg[4]))
            ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
        except IndexError:
            try:
                msg = str(convert(msg[1], msg[2], msg[3]))
                ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
            except (KeyError, IndexError, ValueError):
                msg = MAN_CONVERT

    elif msg[0] == 'timeseries':
        try:
            data = timeseries(msg[1], msg[2], msg[3:])
            msg = json.dumps(data, indent=2)
            ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
        except:
            try:
                data = timeseries(msg[1], msg[2])
                msg = json.dumps(data, indent=2)
                ServerFrame.logging(repr(addr) + ' use latest\n')  # log this
            except (KeyError, IndexError, HTTPError):
                msg = MAN_TIMESERIES

    elif msg[0] == 'logout':
        msg = 'Logging out'
    elif msg[0] == 'quit':
        msg = 'Quitted'
    else:
        msg = MAN_SHELL
    return msg

def interpret_before_handler(msg, addr):
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
        msg = 'You must login first!\n' + MAN_LOGIN
    return msg

def handler(conn, addr):
    logout = False
    while not logout:
        msg = yield from loop.recv(conn, 1642500)
        if not msg:
            conn.close()
            break
        msg = interpret(msg.decode(), addr)
        if msg == 'Quitted':
            ServerFrame.logging(repr(addr) + ' quitted\n')  # log this
            yield from loop.send(conn, msg.encode())
            conn.close()
            break
        elif msg == 'Logging out':
            ServerFrame.logging(repr(addr) + ' logging out\n')  # log this
            loop.create_task((before_handler(conn, addr), None))
            logout = True

        yield from loop.send(conn, msg.encode())

def before_handler(conn, addr):
    logged = False
    while not logged:
        msg = yield from loop.recv(conn, 1024)
        if not msg:
            conn.close()
            break
        msg = interpret_before_handler(msg.decode(), addr)
        if msg == 'Quitted':
            ServerFrame.logging(repr(addr) + ' quitted\n')  # log this
            yield from loop.send(conn, msg.encode())
            conn.close()
            break
        elif msg == 'Account successfully registered':
            ServerFrame.logging(repr(addr) + ' registered an account\n')    # log this
        elif msg == 'True':
            msg = 'Logged in successfully'
            ServerFrame.logging(repr(addr) + ' logged in\n')    # log this
            loop.create_task((handler(conn, addr), None))
            logged = True
        msg = msg.encode()
        yield from loop.send(conn, msg)

conns = []

def main():
    while True:
        conn, addr = yield from loop.accept(s)
        conns.append(conn)
        ServerFrame.logging(repr(addr) + ' connected\n')    # log this
        conn.setblocking(False)
        loop.create_task((before_handler(conn, addr), None))

def close_cuc_suc():
    for conn in conns:
        conn.close()

class ServerGUIThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        app = App()
        app.mainloop()


gui = ServerGUIThread()     # maintain GUI
gui.start()
timer = TimerThread(1800)   # maintain timer for database updating every 30 minutes
timer.start()
loop.create_task((main(), None))
loop.run()
