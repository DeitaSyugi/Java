import psycopg2
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((16, 16), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 256.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)


conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="sayhello", database="postgres")
cur = conn.cursor()
number = 297607
imghash = 0
keyword = 'Kuangjiatu'

#filePath = raw_input("Enter filepath:")
filePath = '/home/python/360Pic/' + keyword
for parent, dirnames, filenames in os.walk(filePath):
    for filename in filenames:
        currentPath = os.path.join(parent, filename)
        #print('the full name of the file is:' + currentPath)
        number += 1
        try:
	    imghash = avhash(currentPath)
            strsql = 'insert into image values(' + str(number) + ',\'' + filename + '\',' + str(
                imghash) + ',\'' + keyword + '\',\'' + currentPath + '\')'
	    cur.execute(strsql)
	    conn.commit()
	except Exception as e:
	    print(e)
	    continue
	if number % 1000 == 0:
	    print(number)

# cur.execute('select * from image')
# rows = cur.fetchall()


cur.close()
conn.close()
