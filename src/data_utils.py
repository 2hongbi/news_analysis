import re

import pandas as pd
import os.path
import time
from hanspell import spell_checker
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('../driver\\chromedriver', options=chrome_options)


def hanspell_checking(sentence):
    sent = spell_checker.check(sentence)
    return sent.checked


def remove_tags(text):
    # (), [] 및 사이 단어들 제거
    pattern = '[\(\[].*?[\)\]]'
    text = re.sub(pattern, repl='', string=text)

    # 특수문자들
    pattern = '[-=+,#/\?:^$.@*\"※~&ㆍ‥!』\\‘|\(\)\[\]\<\>`\'…\"\“”》]'
    text = re.sub(pattern, repl='', string=text)

    # 공백 제거
    # text = text.replace(" ", "")

    return text


# 개선 필요 / 시간이 오래 걸려 현재 spell_checking 함수는 사용하지 않음
def spell_checking(sentence):
    # 한국어 맞춤법/문법 검사기
    # for i in tqdm(range(len(sentence))):
    time.sleep(1)
    driver.get('https://speller.cs.pusan.ac.kr/')
    driver.find_element_by_xpath('//*[@id="text1"]').send_keys(sentence)
    driver.find_element_by_xpath('//*[@id="btnCheck"]').click()
    time.sleep(1)
    num = 0
    while True:
        try:
            error = driver.find_element_by_xpath('//*[@id="tdErrorWord_' + str(num) + '"]/ul/li/a').text
            replace = driver.find_element_by_xpath('//*[@id="tdReplaceWord_' + str(num) + '"]/ul/li/a').text
            sentence = sentence.replace(error, replace)
            num += 1
        except NoSuchElementException as e:
            print('[ERROR] NO FOUND')
            break
    return sentence


def extract_comments(file, output, type='nv'):
    # xlsx 파일 댓글 내용만 추출하여 csv 파일 만드는 함수
    df = pd.read_excel(file)
    column = ['내용', '추천수']
    if type == 'yt':
        column = ['comment', 'num_likes']
    if os.path.isfile(output):
        df.to_csv(output, sep=',', na_rep='NaN', columns=column, index=False, mode='a', encoding='utf-8-sig',
                  header=['comment', 'num_likes'])
    else:
        df.to_csv(output, sep=',', na_rep='NaN', columns=column, index=False, mode='w', encoding='utf-8-sig',
                  header=['comment', 'num_likes'])


def main():
    nv_file_list = [
        '머니투데이_아프간난민을미군기지로.xlsx',
        'news1_아프간난민수용보도에찬반뜨거워.xlsx',
        '서울신문_전세계아프간난민딜레마.xlsx',
        '한겨레_한국협력한아프간현지인국내이송임박.xlsx',
        '한겨레_아프간피란민한국수용.xlsx',
        '한국일보_한국은선진국난민수용선택의문제아니다.xlsx'
    ]

    for file in nv_file_list:
        extract_comments('./../data/comments/'+file, './../data/all_nanmin_comments_with_likes.csv')
        continue

    yt_file_list = ['channelA_news.xlsx', 'mbc_news.xlsx']

    for file in yt_file_list:
        extract_comments('./../data/comments/'+file, './../data/all_nanmin_comments_with_likes.csv', type='yt')