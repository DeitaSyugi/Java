# encoding:UTF-8
import urllib.request
import re

urlRaw = r"https://s.taobao.com/search?q=%E4%BC%91%E9%97%B2%E5%A5%97%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170830&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="
keyword = "casual"

for i in range(0,4400,44):
    url = urlRaw + str(i)
    data = urllib.request.urlopen(url).read()
    data = data.decode('UTF-8')

    reg = r'"pic_url":"//(.+?)"'
    imgReg = re.compile(reg)
    imgLists = imgReg.findall(data)

    print(i)
    fileName = keyword + 'Url.json'
    for imgUrl in imgLists:
        with open(fileName, 'a') as fileObj:
            fileObj.write(imgUrl)
            fileObj.write('\n')
