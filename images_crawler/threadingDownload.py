import threading
import json
import urllib.request

keyword = 'sports'
i = 0
lock = threading.RLock()
imgUrls = []
with open(keyword + 'Url.json', 'r') as file_ob:
    imgUrl = file_ob.readline()
    while imgUrl:
        imgUrls.append(imgUrl)
        imgUrl = file_ob.readline()
print(len(imgUrls))

def spider():
    while True:
        imgdata = imgUrls.pop(0)
        imgdata = 'http://' + imgdata
        global i
        try:
            urllib.request.urlretrieve(imgdata, './{}/{}.jpg'.format(keyword, i))
        except Exception as e:
            print(e)
        lock.acquire()
        i += 1
        lock.release()
        print(i)

for j in range(32):
    t = threading.Thread(target=spider, args=())
    t.start()
t.join()