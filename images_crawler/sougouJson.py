import json
import requests
import re

word = "Liuchengtu"
url = "http://pic.sogou.com/pics?query=%C1%F7%B3%CC%CD%BC&mode=1&start="
urlEnd = "&reqType=ajax&reqFrom=result&tn=0"
with open("sougou_LCT.txt", 'w') as file_object:
    for i in range(48, 1000000, 48):
        url += str(i)
        url += urlEnd
        #url += str(hex(i))
        stdout = requests.get(url)
        jsonData = json.loads(stdout.text)
        for j in range(0, 48):
	    try:
		imgUrl = jsonData["items"][j]["pic_url"]
	    except IndexError:
		print("j=%d, IndexError" %j)
		continue
	    #match = re.search(reg, str(imgUrl))
            #if match: continue
            #if len(str(imgUrl)) < 5: continue
            file_object.write(imgUrl)
            file_object.write("\n")
	print(i)

