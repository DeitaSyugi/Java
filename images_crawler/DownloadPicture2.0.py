# -*-coding:utf-8 -*-
import re
import json
import os
import urllib.request
import socket

socket.setdefaulttimeout(4.0)
dir = "/home/temp"
if not os.path.isdir(dir):
    os.makedirs(dir)

with open("360_KJT.txt") as file_ob:
    i = 0
    keyword = 'Kuangjiatu'
    record = {'Kuangjiatu': 0}
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')]
    urllib.request.install_opener(opener)
    eachline = file_ob.readline()
    while eachline:
        eachline = file_ob.readline()
        string = dir + keyword + '_' + str(i) + eachline[-5:-1]
        try:
            urllib.request.urlretrieve(eachline, string)
        except Exception as e:
            print(e)
            i += 1
            with open("./kjtRecord.json", 'w') as file_json:
                record['Kuangjiatu'] = i
                json.dump(record, file_json)
            continue
        i += 1
        print(i)
        with open("./kjtRecord.json", 'w') as file_json:
            record['Kuangjiatu'] = i
            json.dump(record, file_json)

