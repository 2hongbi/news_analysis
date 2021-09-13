import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


# 크롤링 페이지 설정
news_url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={}'

# 뉴스 검색 키워드를 넣어서 get 요청
query = "아프간 난민 수용"
req = requests.get(news_url.format(query))

# BeautifulSoup 함수 사용 파싱
soup = BeautifulSoup(req.text, 'html.parser')

# 데이터 저장 및 크롤링 페이지 설정
news_dict = []
idx = 0
