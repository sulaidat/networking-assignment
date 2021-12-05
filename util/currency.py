#!/usr/bin/env python3
import json
import requests
from datetime import date
import os

dirname = os.path.dirname(__file__)

db = os.path.join(dirname, '../database/')
baseURL = 'http://api.exchangeratesapi.io/v1/'
key = 'access_key=b7d06743100d59caa9b2c50909defbff'
today = date.today().isoformat()

def fetch_latest(): 
    request = ''.join((baseURL, 'latest?', key))
    data = requests.get(request).json()
    
    fileName = db + today + '.json'
    with open(fileName, "w") as file:
        json.dump(data, file)
    return data

def fetch_historical(date):
    request = ''.join((baseURL, date, '?', key))
    data = requests.get(request).json()

    fileName = db + date + '.json'
    with open(fileName, "w") as file:
        json.dump(data, file)
    return data

def get(date):
    fileName = ''.join((db, date, '.json'))
    try:
        with open(fileName, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        if date == today:
            fetch_latest()
        else:
            fetch_historical(date)
        with open(fileName, "r") as file:
            data = json.load(file)  
    return data

def historical(date, list=None):
    data = get(date)['rates']
    if list:
        return {key.upper():data[key.upper()] for key in list}
    return data

def latest(list=None):
    data = get(today)['rates']
    if list:
        return {key.upper():data[key.upper()] for key in list}
    return data

def convert(src, dst, amount, date=None):
    if not date:
        date = today
    data = get(date)['rates']
    src = data[src.upper()]
    dst = data[dst.upper()]
    return dst*amount / src

def help():
    infomation = """
    Slaydark's Currency Interactive Shell
    
    Commands:
        latest

    Run 'help' for more information
    """
    print(infomation)