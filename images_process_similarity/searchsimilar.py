import psycopg2
import sys
import json
from PIL import Image


def hamming(h1, h2):
    h1, h2 = long(h1), long(h2)
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((16, 16), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 256.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)

h = raw_input("please input the image name: ")
h = avhash(h)
#h = 'LCT_59427.jpg'
conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="sayhello", database="postgres")
cur = conn.cursor()
#cur.execute(r"select hash from image where name='%s'" %h)
#conn.commit()
#try:
#    h = cur.fetchall()
#    h = h[0][0]
#except Exception as e:
#    print("Can not find this name in database!!")
#    sys.exit()

cur.execute(r"select hash,name from image")
conn.commit()
rows = cur.fetchall()

cur.execute(r"select count(*) from image")
conn.commit()
countnum = cur.fetchall()
countnum = countnum[0][0]

images = []
seq = []
i = 20
prog = 1
for row in rows:
    hashed = row[0]
    name = row[1]
    seq.append((name, hamming(hashed, h), hashed))
    if prog:
	perc = 100. * prog / countnum
	x = int(2 * perc / 5)
	print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
        print '%.2f%%' % perc, '(%d/%d)' % (prog, countnum),
        sys.stdout.flush()
        prog += 1
print
jsondata = []
hashlists = []
for f,ham,hashlist in sorted(seq, key=lambda j: j[1]):
    if hashlist in hashlists:
	continue
    print("%d\t%s" % (ham, f))
    hashlists.append(hashlist)
    jsondata.append(f)
    i += -1
    if i == 0:
        break


with open('./similarImage.json', 'w') as json_file:
    json.dump(jsondata, json_file)

cur.close()
conn.close()
