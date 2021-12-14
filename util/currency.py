#!/usr/bin/env python3
# currency.py
"""
This module provides some exchange rate API
"""

import json
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import date, timedelta
import os

cwd = os.path.abspath(os.getcwd())
db = os.path.join(cwd, 'database/')

if not os.path.exists(db):
    os.makedirs(db)

baseURL = 'http://api.exchangeratesapi.io/v1/'
key = 'access_key=b7d06743100d59caa9b2c50909defbff'
today = date.today().isoformat()

def fetch_latest(): 
    request = ''.join((baseURL, 'latest?', key))
    data = json.loads(urlopen(request).read().decode())
    
    fileName = db + today + '.json'
    with open(fileName, "w") as file:
        json.dump(data, file)
    return data

def fetch_historical(date):
    request = ''.join((baseURL, date, '?', key))
    data = json.loads(urlopen(request).read().decode())

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
        elif not os.path.isfile(fileName):
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
    return dst*float(amount) / src

def timeseries(start_date, end_date, base, symbols_list=None):
    if symbols_list:
        symbols_list = ','.join(i.upper() for i in symbols_list)
    else:
        symbols_list = 'None'

    request = 'https://api.exchangerate.host/timeseries?' \
        + 'start_date=' + start_date \
        + '&end_date=' + end_date \
        + '&base=' + base.upper() \
        + '&symbols=' + symbols_list 
    # print(request)
    try:
        data = json.loads(urlopen(request).read().decode())['rates']
    except HTTPError:
        data = None
    
    return data