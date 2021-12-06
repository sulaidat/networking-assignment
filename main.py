#!/usr/bin/env python3
import json
import requests

baseURL = "http://api.exchangeratesapi.io/v1/"
key = "b7d06743100d59caa9b2c50909defbff"





def shell():
    help()
    while True:
        x = input("hacdao> ")
        if x == 'exit':
            break
        if x == 'help':
            help()
        elif x == 'latest':
            latest()  


def fetch_latest(baseURL, key, fileName): 
    request = baseURL + 'latest?access_key=' + key
    print(request)
    response = requests.get(request)
    data = response.json()
    with open(fileName, "w") as file:
        json.dump(data, file)

if __name__ == '__main__':
    # latest(baseURL, key, 'db.json')
    shell()
