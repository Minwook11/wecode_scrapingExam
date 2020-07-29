from bs4 import BeautifulSoup
from selenium import webdriver # 브라우저를 열수 있는 드라이브모듈
from selenium.webdriver.common.keys import Keys # 키이벤트를 돕는 키 모듈
import requests
import re
import csv
import time

def url_extract(line):
    url_start = line.find('(') + 1
    url_end = line.find(')') - 1

    return line[url_start : url_end]

csv_filename = "billboard_crawl.csv"
csv_open = open(csv_filename, "w+", encoding='utf-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow( ('rank', 'title', 'singer', 'cover url') )

orig_url = 'https://www.billboard.com/charts/hot-100' # 크롤링 할 사이트

driver = webdriver.Chrome('/usr/bin/chromedriver') # 크롬 브라우저 선택
driver.implicitly_wait(10) # 숫자 크면 잘 읽히는 기붕..
driver.get(orig_url) # 입력한 경로의 정보 긁어볼까요~?
body = driver.find_element_by_css_selector('body') # send_keys()메서드 사용을 위한 body가져오기

for i in range(20): # 11번 ~ 최하단 20번 
    body.send_keys(Keys.PAGE_DOWN) # 페이지 다운 키를  20회 반복한다.
    time.sleep(0.1) # 페이지 로드 대기, 숫자가 크면 안읽히는건 왤까요?


# beautifulsoup 사용 하기 준비
html = driver.page_source # html을 문자열로 가져온다.
driver.close()  # 크롬드라이버 창닫기

bs = BeautifulSoup(html, 'html.parser' )

li_list = bs.find_all('li', {'class': re.compile('chart-list__element')})

for li in li_list:    
    song_rank = li.find_all('span', {'class': re.compile('chart-element__rank__number')})   # 찾아온 <li> 태그의 데이터 중 <span> 태그의 chart-element__rank__number 클래스 데이터를 찾는다.
    song_title = li.find_all('span', {'class': re.compile('chart-element__information__song')})     # 상동, 클래스 이름은 chart-element__information__song
    song_singer = li.find_all('span', {'class': re.compile('chart-element__information__artist')})      # 상동, 클래스 이름은 chart-element__information__artist
    song_cover = li.find_all('span', {'class': re.compile('chart-element__image')})     # 상동, 클래스 이름은 chart-element__image

    rank = song_rank[0].text

    title = song_title[0].text

    singer = song_singer[0].text

    cover = url_extract(str(song_cover))

    csv_writer.writerow( (rank, title, singer, cover) )

csv_open.close()
