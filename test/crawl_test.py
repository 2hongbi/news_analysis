from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd  # pandas, openpyxl
import time


def get_replys(url, imp_time=5, delay_time=0.1):
    #웹 드라이버
    driver = webdriver.Chrome('./../driver/chromedriver.exe')
    driver.implicitly_wait(imp_time)
    driver.get(url)

    #더보기 계속 클릭하기
    while True:
        try:
            deobogi = driver.find_element_by_css_selector('a.u_cbox_btn_more')
            deobogi.click()
            time.sleep(delay_time)
        except:
            break

    html = driver.page_source
    # print(html)

    # 모듈 참조
    soup = BeautifulSoup(html, 'lxml') #html.parser

    '''
    # 기사제목 추출
    article_head = driver.find_element_by_css_selector('div.article_info > h3 > a')
    print('기사 제목 : ', article_head[0].text)

    # 기사시간 추출
    article_time = driver.find_element_by_css_selector('div.sponsor > span.t11')
    print('기사 등록 시간 : ', article_time[0].text)

    # 성비와 연령대 추출
    per = driver.find_elements_by_css_selector('span.u_cbox_chart_per')

    print("남자 성비 : " + per[0].text)
    print("여자 성비 : " + per[1].text)
    print("10대 : " + per[2].text)
    print("20대 : " + per[3].text)
    print("30대 : " + per[4].text)
    print("40대 : " + per[5].text)
    print("50대 : " + per[6].text)
    print("60대 이상 : " + per[7].text)
    '''

    # 댓글추출
    contents = soup.select('span.u_cbox_contents')
    contents = [content.text for content in contents]

    #작성자
    nicks = soup.select('span.u_cbox_nick')
    nicks = [nick.text for nick in nicks]

    #날짜 추출
    dates = soup.select('span.u_cbox_date')
    dates = [date.text for date in dates]

    # 취합
    replys = list(zip(nicks, dates, contents))

    driver.quit()

    return replys


if __name__ == '__main__':

    start = datetime.now()

    url_list = {
        '머니투데이_아프간난민을미군기지로.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=102&oid=008&aid=0004634396',
        'news1_아프간난민수용보도에찬반뜨거워.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=102&oid=421&aid=0005555453',
        '서울신문_전세계아프간난민딜레마.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=104&oid=081&aid=0003210731',
        '한겨레_한국협력한아프간현지인국내이송임박.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=100&oid=028&aid=0002557848',
        '한겨레_아프간피란민한국수용.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=100&oid=028&aid=0002557561',
        '한국일보_한국은선진국난민수용선택의문제아니다.xlsx': 'https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=102&oid=469&aid=0000628032'
    }

    for title in url_list:
        url = url_list[title]
        reply_data = get_replys(url, 5, 0.1)


        col =['작성자', '날짜', '내용']
        data_frame = pd.DataFrame(reply_data,columns=col)
        data_frame.to_excel(title, startrow=0, header=True)


    end = datetime.now()
    print(end-start)