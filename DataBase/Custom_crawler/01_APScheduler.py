import requests
from bs4 import BeautifulSoup
import time
from apscheduler.schedulers.background import BlockingScheduler

def create_soup(url):
    ## headers는 host로부터 강제로 연결이 끊겼을때 추가해주면 됨
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()    

    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def scrape_weather():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%82%A0%EC%94%A8&oquery=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%8B%9C&tqi=hxmTBsp0J14ssMrx29KssssssPR-110721"
    soup = create_soup(url)
    
    source = soup.find("strong",{"class":"provider _provider"}).get_text()
    
    ## 어제보다 문구 해결 ##
    summary_list = [] ## 어제보다 OO 맑음 or 흐림
    summary_temp_list = soup.find("p", {"class":"summary"}).get_text().split(' ')
    for summary in summary_temp_list:
        if summary != '':
            summary_list.append(summary)
    
    ## 현재 강수확률 문구 해결 ##
    cell_weather = soup.find("div",{"class":"day_data"})
    today = cell_weather.find("span",{"class":"date"}).get_text()
    rainfall_rate_am = cell_weather.find_all("span",{"class":"weather_left"})[0].get_text().strip().split(' ') # [오전, 강수확률]
    rainfall_rate_pm = cell_weather.find_all("span",{"class":"weather_left"})[1].get_text().strip().split(' ') # [오후, 강수확률]

    ## 현재 온도 문구 해결 ##
    curr_temperature = soup.find("div", {"class":"temperature_text"}).get_text().strip().replace(" 온도", ": ")

    ## 최저 / 최고 온도 문구 해결 ##
    temp_lowest = cell_weather.find("span",{"class":"lowest"}).get_text().replace("기온", ': ')
    temp_highest = cell_weather.find("span",{"class":"highest"}).get_text().replace("기온", ': ')

    print()
    print(f"[오늘({today[:-1]})의 날씨 브리핑 ({source} 제공)] ")
    print('-'*90)
    print(f"{curr_temperature} ({temp_lowest} / {temp_highest})")
    print(f"{summary_list[-1]}, {summary_list[0]} {summary_list[1]} {summary_list[2]}")
    print(f"{rainfall_rate_am[0]} 강수확률: {rainfall_rate_am[1]} / {rainfall_rate_pm[0]} 강수확률: {rainfall_rate_pm[1]}")
    print()
    print()
    
def scrape_headline_news():
    naver_news_url = 'https://news.naver.com'
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101" ## 경제분야
    soup = create_soup(url)
    
    ## 헤드라인 기사들의 link들 ##
    article_title = [] # 헤드라인 기사제목
    article_link = [] # 헤드라인 기사들의 link
    for idx in range(5):
        article_title.append(soup.find_all("h2", {"class":"cluster_head_topic"})[idx].get_text().strip())
        article_link.append(naver_news_url+soup.find_all("a", {"class":"nclicks(cls_eco.clstitle)"})[idx*2]["href"])
    today_article = soup.find("span", {"class":"lnb_date"}).get_text().strip()
    print(f"[{today_article}  경제 헤드라인 뉴스 5]")
    print('-'*90)
    for idx, title, link in zip(range(5), article_title, article_link):
        print(f"({idx+1}) {title}")
        print(f"   (링크: {link})")
    print()
    print()

def scrape_it_news():
    naver_news_url = 'https://news.naver.com'
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105" ## 경제분야
    soup = create_soup(url)
    
    ## 헤드라인 기사들의 link들
    article_title = [] # 헤드라인 기사제목
    article_link = [] # 헤드라인 기사들의 link
    for idx in range(5):
        article_title.append(soup.find_all("h2", {"class":"cluster_head_topic"})[idx].get_text().strip()) # 기사 제목
        article_link.append(naver_news_url+soup.find_all("a", {"class":"nclicks(cls_sci.clstitle)"})[idx*2]["href"]) # 기사 링크
    
    today_article = soup.find("span", {"class":"lnb_date"}).get_text().strip() # 오늘의 날짜
    print(f"[{today_article}  IT 헤드라인 뉴스 5]")
    print('-'*90)
    for idx, title, link in zip(range(5), article_title, article_link):
        print(f"({idx+1}) {title}")
        print(f"   (링크: {link})")


def main():
    sched = BlockingScheduler(timezone='Asia/Seoul')
    print(f'스크래핑 시간 : {time.strftime("%H:%M:%S")}')
    sched.add_job(scrape_weather, 'cron', hour='8-9', minute=0, second=1, id='test')
    sched.add_job(scrape_headline_news,'cron', hour='8-9', minute=0, second=2, id='test1')
    sched.add_job(scrape_it_news, 'cron', hour='8-9', minute=0, second=3, id='test2')
    sched.start()

if __name__ == "__main__":
    main()
