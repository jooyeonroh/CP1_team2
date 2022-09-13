# 상위 폴더에 있는 파일 import할 때 사용
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DataBase'))))

import database_connection
import csv

f = open('소비기한 관련 뉴스기사(~2022-09-08)(1).csv', 'r', encoding='utf-8')
reader = csv.reader(f)
next(reader)

# (1) idx (2) news_title (3) news_press (4) posted_data (5) news_link
conn, cur = database_connection.postgreconn()
cur.execute("DROP TABLE IF EXISTS article;")
cur.execute("""CREATE TABLE article(
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    dsc TEXT,
                    press VARCHAR(20),
                    posted_date DATE,
                    link TEXT);""")
conn.commit()
for data in reader:
    print(data)
    cur.execute("INSERT INTO article(id, title, dsc, press, posted_date, link) VALUES(%s, %s, %s, %s, %s, %s)", data)

conn.commit()
conn.close()


