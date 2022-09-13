import csv
import requests
import time
import random
from bs4 import BeautifulSoup

# BeautifulSoup 실행 함수
def bs4_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup    

def article_crawler():
    filename = '소비기한 관련 뉴스기사(~2022-09-08).csv'
    f = open(filename, "w", encoding='utf-8-sig', newline='')
    writer= csv.writer(f)

    columns = "N, news_title, news_press, posted_date, news_link".split(', ')
    writer.writerow(columns)

    news_title_list = []
    news_press_list = []
    news_posted_date_list = []
    news_link_list = []
    ## 다음뉴스에서 가져온 소비기한 타이틀 뉴스 ##
    for idx in range(1000):
        time.sleep(random.uniform(1,5))
        url = f'https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=%EC%86%8C%EB%B9%84%EA%B8%B0%ED%95%9C+%ED%91%9C%EC%8B%9C%EC%A0%9C&sd=20210601000000&ed=20220908235959&sort=accuracy&period=u&p={idx}'
        soup = bs4_soup(url)

        news_all = soup.find_all("div", {"class":"wrap_cont"})
        for news in news_all:
            if '소비기한' in news.find("a").get_text().strip(): 
                print("기사 제목:",news.find("a").get_text().strip())
                news_title_list.append(news.find("a").get_text().strip())
                print("언론사:",news.find("span",{"class":"cont_info"}).get_text().strip().split(' ')[0])
                news_press_list.append(news.find("span",{"class":"cont_info"}).get_text().strip().split(' ')[0])
                print("게시 일자:",news.find("span",{"class":"cont_info"}).get_text().strip().split(' ')[1].replace(".","-"))
                news_posted_date_list.append(news.find("span",{"class":"cont_info"}).get_text().strip().split(' ')[1].replace(".","-"))
                print("기사 링크:",news.find("a")['href']) # 기사링크
                news_link_list.append(news.find("a")['href'])
                print()
            else:
                continue
                # print("해당 뉴스헤드라인에는 소비기한이 없습니다.")
        print(f"{idx}page - 총 {len(news_title_list)}의 뉴스를 수집했습니다.")

    for idx, news in enumerate(zip(news_title_list, news_press_list, news_posted_date_list, news_link_list)):
        writer.writerow([idx+1, news[0], news[1], news[2], news[3]]) ## writerow에는 꼭 list화 해야 함

    f.close()

if __name__ == "__main__":
    article_crawler()