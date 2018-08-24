# -*-coding:utf-8 -*-
import re
import requests
import json
import os
import urllib.request
import socket

socket.setdefaulttimeout(4.0)
dir = "./360Pic/Liuchengtu"
if not os.path.isdir(dir):
    os.makedirs(dir)
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'file.001pp.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

}
with open("360_LCT.txt") as file_ob:
    i = 0
    keyword = 'LCT'
    record = {'Biaoge': 0, 'Liuchengtu': 0, 'kuangjiatu': 0}
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')]
    urllib.request.install_opener(opener)
    eachline = file_ob.readline()
    while eachline:
        eachline = file_ob.readline()
        # host = re.findall('http://(.*?)/', eachline, re.S)
        # headers['Host'] = host[0]
        string = './360Pic/Liuchengtu/' + keyword + '_' + str(i) + eachline[-5:-1]
        try:
            # session = requests.Session()
            # session.max_redirects = 60
            # pic = session.get(eachline, timeout=5, headers=headers)
            urllib.request.urlretrieve(eachline, string)
        except Exception as e:
            print(e)
            # print("Error, can not download this picture!")
            i += 1
            with open("./record.json", 'w') as file_json:
                record['Liuchengtu'] = i
                json.dump(record, file_json)
            continue
        # with open(string.decode('utf-8').encode('cp936'), 'wb') as fp:
        #     fp.write(pic.content)
        i += 1
        print(i)
        with open("./record.json", 'w') as file_json:
            record['Liuchengtu'] = i
            json.dump(record, file_json)

