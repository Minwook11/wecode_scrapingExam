from selenium import webdriver
from bs4 import BeautifulSoup

import re
import csv

def tag_Clear(arg):     # <dd></dd> 태그 제거 목적용 함수 사용
    return arg[4:(len(arg) - 5)]        # 문자열 슬라이스

csv_filename = "starbucks_crawl.csv"
csv_open = open(csv_filename, "w+", encoding='utf-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow( ('name', 'img') )

target_url = 'https://www.starbucks.co.kr/menu/drink_list.do'   # 크롤링 할 사이트
driver = webdriver.Chrome('/usr/bin/chromedriver') 

driver.implicitly_wait(5)   # 5초 대기함
driver.get(target_url)      # 페이지 소스 받아오기

html = driver.page_source 

driver.close()
driver.quit()

bs = BeautifulSoup(html, 'html.parser')     # 받아온 HTML 소스 파싱을 위한 BS 객체

menu_full_list = bs.find_all('li', {'class': re.compile('menuDataSet')})    # menuDataSet 클래스명으로 li태그를 전부 찾기

for each_list in menu_full_list:    # 태그 하나하나에 적용한다.
    menu_name = tag_Clear(str(each_list.find('dd')))    # <dd> 태그로 감싸진 메뉴 이름을 찾아서 저장
    # menu_name = each_list.find('dd')
    menu_img_full = each_list.find('img')   # <img> 태그로 감싸진 요소를 저장
    menu_img = menu_img_full.get('src')     # <img> 태그의 'src' 항목을 저장

    csv_writer.writerow( (menu_name, menu_img) )    # 이름과 링크를 한 줄에 저장

csv_open.close()