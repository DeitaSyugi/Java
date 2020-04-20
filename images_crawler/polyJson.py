import json
import requests
import re


url = r"https://www.polyvore.com/cgi/search.sets?.in=json&.out=jsonx&request=%7B%22query%22%3A%22activewear%22%2C%22.search_src%22%3A%22masthead_search%22%2C%22page%22%3Anull%2C%22.passback%22%3A%7B%22next_token%22%3A%7B%22limit%22%3A%2230%22%2C%22start%22%3A"
endurl = "%7D%7D%7D"
keyword = 'Activewear'
jsonfile = 'ployvoreJson' + keyword + '.json'
imgdatas = []
for i in range(30, 900, 30):
    finalurl = url
    finalurl += str(i)
    finalurl += endurl
    stdout = requests.get(finalurl)
    # jsondata = json.loads(stdout.text)
    html = stdout.text
    reg = r'src=\\"(.+?)\\" alt='
    reg2 = r'alt=\\"(.+?)\\"'
    imgre = re.compile(reg)
    imglists = imgre.findall(html)
    describelists = re.compile(reg2).findall(html)
    if len(imglists) != len(describelists):
        print("The imglists is not equal to describelists!!")
        break
    for index, img in enumerate(imglists):
        imgdata = {}
        describe = describelists[index]
        imgdata['imgurl'] = img
        imgdata['imgdescribe'] = describe
        imgdatas.append(imgdata)
    print(i)
    with open(jsonfile, 'w') as file_ob:
        json.dump(imgdatas, file_ob)
