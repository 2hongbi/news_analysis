import pandas as pd
import os.path
import time
from selenium import webdriver
from tqdm import tqdm

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('../driver\\chromedriver', options=chrome_options)


def spell_checking(sentence):
    # for i in tqdm(range(len(sentence))):
    try:
        time.sleep(0.5)
        driver.get('https://speller.cs.pusan.ac.kr/')
        driver.find_element_by_xpath('//*[@id="text1"]').send_keys(sentence)
        driver.find_element_by_xpath('//*[@id="btnCheck"]').click()
        time.sleep(1)
        num = 0
        while True:
            try:
                replace = driver.find_element_by_xpath('//*[@id="tdReplaceWord_' + str(num) + '"]/ul/li/a').text
                print(replace)
                num += 1
            except:
                # didnt know the exact cause of exception -> 일단은 bare하게 처리
                print('[ERROR] spell_checking NUM :', num)
                break
        texts = driver.find_element_by_xpath('//*[@id="tdCorrection1stBox"]').text
        print(texts)
    finally:
        driver.close()

def extract_comments(file, output, type='nv'):
    # xlsx 파일 댓글 내용만 추출하여 csv 파일 만드는 함수
    df = pd.read_excel(file)
    column = ['내용']
    if type == 'yt':
        column = ['comment']
    if os.path.isfile(output):
        df.to_csv(output, sep=',', na_rep='NaN', columns=column, index=False, mode='a', encoding='utf-8-sig',
                  header=False)
    else:
        df.to_csv(output, sep=',', na_rep='NaN', columns=column, index=False, mode='w', encoding='utf-8-sig',
                  header=False)


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
        extract_comments('./../data/comments/'+file, './../data/all_nanmin_comments.csv')
        continue

    yt_file_list = ['channelA_news.xlsx', 'mbc_news.xlsx']

    for file in yt_file_list:
        extract_comments('./../data/comments/'+file, './../data/all_nanmin_comments.csv', type='yt')