#!/usr/bin/env python3
# timer.py

from threading import Thread, Event
from util.currency import fetch_latest
import time

class MyThread(Thread):
    def __init__(self, timeout):
        Thread.__init__(self)
        self.event = Event()
        self.timeout = timeout
    def run(self):
        while not self.event.wait(self.timeout):
            fetch_latest()
            print("update!")
