import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DataBase'))))

import database_connection
import csv
import requests
import time
import random
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

# BeautifulSoup 실행 함수
def bs4_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers) # headers=headers
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup    

def article_crawler():
    print(f'스크래핑 시작시간 : {time.strftime("%H:%M:%S")}')

    filename = f'소비기한 관련 뉴스기사{time.strftime("%y-%m-%d")}.csv'
    f = open(filename, "w", encoding='utf-8-sig', newline='')
    writer= csv.writer(f)

    columns = "news_title, desc, news_press, posted_date, news_link".split(', ')
    writer.writerow(columns)

    news_title_list = []
    news_desc_list = []
    news_press_list = []
    news_posted_date_list = []
    news_link_list = []

    for idx in range(1, 20, 10):
        time.sleep(random.uniform(1,2))
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%86%8C%EB%B9%84%EA%B8%B0%ED%95%9C%20%ED%91%9C%EC%8B%9C%EC%A0%9C&sort=1&photo=0&field=0&pd=3&ds={time.strftime("%Y.%m.%d")}&de={time.strftime("%Y.%m.%d")}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{time.strftime("%Y%m%d")}to{time.strftime("%Y%m%d")},a:all&start={idx}'
        soup = bs4_soup(url)
        news_content = soup.find_all("div", {"class":"news_area"})
        for news in news_content:
            if '소비기한' in news.find("a",{"class":"news_tit"})['title'].strip():
                if len(news.find_all("span", {"class":"info"})) >= 2:
                    print()
                    print("기사 제목:",news.find("a",{"class":"news_tit"})['title'].strip())
                    news_title_list.append(news.find("a",{"class":"news_tit"})['title'].strip())
                    print("기사 요약:",news.find("a",{"class":"api_txt_lines dsc_txt_wrap"}).get_text().strip())
                    news_desc_list.append(news.find("a",{"class":"api_txt_lines dsc_txt_wrap"}).get_text().strip())
                    print("언론 계열 :",news.find("a", {"class":"info press"}).get_text().strip())
                    news_press_list.append(news.find("a", {"class":"info press"}).get_text().strip())
                    print("게시 일자:",time.strftime("%Y-%m-%d"))
                    news_posted_date_list.append(time.strftime("%Y-%m-%d"))        
                    print("기사 링크:",news.find("a",{"class":"news_tit"})['href'].strip())
                    news_link_list.append(news.find("a",{"class":"news_tit"})['href'].strip())
                else:
                    print()
                    print("기사 제목:",news.find("a",{"class":"news_tit"})['title'].strip())
                    news_title_list.append(news.find("a",{"class":"news_tit"})['title'].strip())
                    print("기사 요약:",news.find("a",{"class":"api_txt_lines dsc_txt_wrap"}).get_text().strip())
                    news_desc_list.append(news.find("a",{"class":"api_txt_lines dsc_txt_wrap"}).get_text().strip())
                    print("언론 계열 :",news.find("a", {"class":"info press"}).get_text().strip())
                    news_press_list.append(news.find("a", {"class":"info press"}).get_text().strip())
                    print("게시 일자:",time.strftime("%Y-%m-%d"))
                    news_posted_date_list.append(time.strftime("%Y-%m-%d"))        
                    print("기사 링크:",news.find("a",{"class":"news_tit"})['href'].strip())
                    news_link_list.append(news.find("a",{"class":"news_tit"})['href'].strip())
            else:
                continue
        print(f"{(idx//10)+1} page. {len(news_title_list)}개 수집되었습니다.")

    for news in zip(news_title_list, news_desc_list ,news_press_list, news_posted_date_list, news_link_list):
        writer.writerow([news[0], news[1], news[2], news[3], news[4]]) ## writerow에는 꼭 list화 해야 함

    f.close()

def dbloads():
    print()
    print(f'스크래핑 적재시간 : {time.strftime("%H:%M:%S")}')
    f = open(f'소비기한 관련 뉴스기사{time.strftime("%y-%m-%d")}.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)

    # (1) idx (2) news_title (3) news_press (4) posted_data (5) news_link
    conn, cur = database_connection.postgreconn()

    for data in reader:
        print(data)
        cur.execute("""INSERT INTO article(id, title, dsc, press, posted_date, link) 
                       VALUES((SELECT MAX(id) FROM article)+1,%s, %s, %s, %s, %s)""", data)

    conn.commit()
    conn.close()

def main():
    sched = BackgroundScheduler(timezone='Asia/Seoul')
    print(f'크롤러 가동시간 : {time.strftime("%H:%M:%S")}')
    sched.add_job(article_crawler, 'cron', hour='8-10', minute=0, second=0, id='test')
    sched.add_job(dbloads, 'cron', hour='8-10', minute= 0, second=20, id='test_2')
    sched.start()

if __name__ == "__main__":
    main()
    while True:
        time.sleep(1)