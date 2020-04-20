# decoding=utf-8
import json
import requests
import re

word = "流程图"
url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%A1%86%E6%9E%B6%E5%9B%BE&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%A1%86%E6%9E%B6%E5%9B%BE&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn="
urlEnd = "&rn=30&gsm="
reg = r'http://img[0-9].imgtn.bdimg.com'
with open("KJT_1.txt", 'w') as file_object:
    for i in range(30, 1000000, 30):
        url += str(i)
        url += urlEnd
        url += str(hex(i))
        stdout = requests.get(url)
        jsonData = json.loads(stdout.text)
        for j in range(0, 29):
            imgUrl = jsonData["data"][j]["replaceUrl"][-1]["ObjURL"]
            match = re.search(reg, str(imgUrl))
            if match: continue
            if len(str(imgUrl)) < 5: continue
            file_object.write(imgUrl)
            file_object.write("\n")
        print(i)
