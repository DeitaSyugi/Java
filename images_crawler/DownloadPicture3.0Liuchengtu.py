# -*-coding:utf-8 -*-
import re
import json
import os
import urllib.request
import socket

socket.setdefaulttimeout(4.0)
dir = "./360Pic/Liuchengtu"
if not os.path.isdir(dir):
    os.makedirs(dir)
record = {'Liuchengtu': 0}
with open("./lctRecord.json") as file_json:
    record = json.load(file_json)
with open("360_LCT.txt") as file_ob:
    i = record['Liuchengtu']
    for x in range(0, i):
        eachline = file_ob.readline()
    keyword = 'Liuchengtu'
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')]
    urllib.request.install_opener(opener)
    eachline = file_ob.readline()
    while eachline:
        eachline = file_ob.readline()
        string = './360Pic/Liuchengtu/' + keyword + '_' + str(i) + eachline[-5:-1]
        try:
            urllib.request.urlretrieve(eachline, string)
        except Exception as e:
            print(e)
            i += 1
            with open("./lctRecord.json", 'w') as file_json:
                record['Liuchengtu'] = i
                json.dump(record, file_json)
            continue
        i += 1
        print(i)
        with open("./lctRecord.json", 'w') as file_json:
            record['Liuchengtu'] = i
            json.dump(record, file_json)

