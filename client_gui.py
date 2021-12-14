#!/usr/bin/env python3
# client.py

import json
import socket
import tkinter as tk 
from tkinter import Listbox, messagebox
from tkinter import ttk
from tkinter.constants import LEFT, RIGHT, VERTICAL, WORD, Y
from tkinter.font import BOLD
from typing import Tuple 
LARGE_FONT = ("verdana", 13,"bold")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5566))


class LatestFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="RoyalBlue4")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(3, weight=1)

        label_title = tk.Label(self, text="Currency Rate", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        label_title.grid(row=0, column=1)
        label_hist = tk.Label(self, text="Latest", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_hist.grid(row=1, column=1)
        label_title = tk.Label(self, text="list", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        label_title.grid(row=2, column=0, sticky='e')

        list_result = tk.Listbox(self)
        scrbar = tk.Scrollbar(list_result, orient=VERTICAL)
        list_result.config(yscrollcommand=scrbar.set)
        scrbar.config(command=list_result.yview)

        scrbar.pack(side=LEFT, fill=Y, expand=True)
        list_result.grid(row=3, column=0, sticky='news', columnspan=3, pady=10, padx=10)

        entry_list = tk.Entry(self, bg='AliceBlue')
        entry_list.grid(row=2, column=1, sticky='ew', padx=10)

        button_go = tk.Button(self,text="GO !",bg="RoyalBlue4",fg='floral white',command=lambda: controller.request_latest(entry_list, list_result)) 
        button_go.grid(row=2, column=2, sticky='w')

        button_latest = tk.Button(self,text="Historical >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(HistoricalFrame)) 
        button_latest.grid(row=4, column=0)
        button_convert = tk.Button(self,text="Convert >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(ConvertFrame)) 
        button_convert.grid(row=4, column=2)
        

        
class HistoricalFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="RoyalBlue4")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(4, weight=1)

        label_title = tk.Label(self, text="Currency Rate", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        label_title.grid(row=0, column=1)
        label_hist = tk.Label(self, text="Historical", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_hist.grid(row=1, column=1)
        label_hist = tk.Label(self, text="date", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_hist.grid(row=2, column=0, sticky='e')
        label_hist = tk.Label(self, text="list", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_hist.grid(row=3, column=0, sticky='e')

        entry_date = tk.Entry(self, bg='AliceBlue')
        entry_date.grid(row=2, column=1, sticky='ew', padx=10)
        entry_item = tk.Entry(self, bg='AliceBlue')
        entry_item.grid(row=3, column=1, sticky='ew', padx=10)

        button_go = tk.Button(self,text="GO !",bg="RoyalBlue4",fg='floral white',command=lambda: controller.search( list_result, entry_date)) 
        button_go.grid(row=3, column=2, sticky='w')

        button_latest = tk.Button(self,text="Latest >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(LatestFrame)) 
        button_latest.grid(row=5, column=0)
        button_convert = tk.Button(self,text="Convert >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(ConvertFrame)) 
        button_convert.grid(row=5, column=2)
        
        list_result = tk.Label(self, text="", bg="floral white", fg='black'  )
        list_result.grid(row=4, column=0, sticky='news', columnspan=3, pady=10, padx=10)

class ConvertFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="RoyalBlue4")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure([0,1,2,3,4,5,6], weight=1)

        label_title = tk.Label(self, text="Currency Rate", font=LARGE_FONT,fg='floral white',bg="RoyalBlue4")
        label_title.grid(row=0, column=1)
        label_convert = tk.Label(self, text="Convert", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_convert.grid(row=1, column=1)

        entry_from = tk.Entry(self,bg='AliceBlue')
        entry_from.grid(row=2, column=1, sticky='ew', padx=10)
        entry_to = tk.Entry(self,bg='AliceBlue')
        entry_to.grid(row=3, column=1, sticky='ew', padx=10)
        entry_amount = tk.Entry(self,bg='AliceBlue')
        entry_amount.grid(row=4, column=1, sticky='ew', padx=10)

        label_from = tk.Label(self, text="from", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_from.grid(row=2, column=0, sticky='e')
        label_to = tk.Label(self, text="to", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_to.grid(row=3, column=0, sticky='e')
        label_amount = tk.Label(self, text="amount", font=LARGE_FONT, fg='floral white',bg="RoyalBlue4")
        label_amount.grid(row=4, sticky='e')
        

        button_go = tk.Button(self,text="GO !",bg="RoyalBlue4",fg='floral white',command=lambda: controller.search( label_amount, entry_from)) 
        button_go.grid(row=4, column=2, sticky='w')
        button_latest = tk.Button(self,text="Latest >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(LatestFrame)) 
        button_latest.grid(row=6, column=0)
        button_his = tk.Button(self,text="Historical >",bg="RoyalBlue4",fg='floral white',command=lambda: controller.showFrame(HistoricalFrame)) 
        button_his.grid(row=6, column=2)
        
        list_result = tk.Label(self, text="", bg="floral white", fg='black'  )
        list_result.grid(row=5, column=1, sticky='news', pady=10, padx=10)        


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("APP")
        self.geometry("500x200")
        self.resizable(width=True, height=True)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LatestFrame, HistoricalFrame, ConvertFrame):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(LatestFrame) 
    def showFrame(self, Frame_name):
        self.frames[Frame_name].tkraise()
    
    def onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
           
    def search(self, list_result, entry_latest):
        try:
            a = "VND: "
            list_result["text"] = ""
            info = entry_latest.get()    
                
            if (info == ""):
                list_result["text"] = "Enter information !"
                return
            else:
                list_result["text"] = a + str(info)
                return
        except:
            list_result["text"] = "Error !"
    
    def request_latest(self, entry_list, list_result):
        # request
        request = 'latest' + entry_list.get()

        s.send(request.encode())
        data = s.recv(4096).decode()
        data = json.loads(data)
        data = json.dumps(data, indent=3)
        print(data)
        # nhan response va bieu dien ra giao dien

        # print(repr(data))
        # for item in data.items():
        #     list_result.insert(str(item)) 

s.send('login tuyen 123'.encode())
s.recv(1024)


app = App()
app.mainloop()
