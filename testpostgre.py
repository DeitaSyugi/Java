import psycopg2

conn = psycopg2.connect(host="127.0.0.1", port="5432", user="postgres", password="sayhello", database="postgres")
cur = conn.cursor()
cur.execute(r"select hash from image")
#print(r"insert into image values(1,'Biage_1.jpg',111111111111,'Biaoge','./sd/sd.jpg')")
conn.commit()
rows = cur.fetchall()
i = 10
for row in rows:
    print(row)
    print(type(row))
    string = row[0]
    print(type(string)) 
    i = i - 1
    if i == 0:
	break

cur.close()
conn.close()
