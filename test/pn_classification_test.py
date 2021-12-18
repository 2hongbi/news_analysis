import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm

from src.data_utils import remove_tags

with open("./../data/words/negative_words_self.txt", encoding='utf-8') as neg:
    negative = neg.readlines()

with open("./../data/words/positive_words_self.txt", encoding='utf-8') as pos:
    positive = pos.readlines()


negative = [neg.replace("\n", "") for neg in negative]
positive = [pos.replace("\n", "") for pos in positive]


labels = []
titles = []


for num in tqdm(range(50)):

    # 이재명
    url = 'https://search.naver.com/search.naver?&where=news&query=이재명&sm=tab_pge&sort=0&photo=0&field=0' \
          '&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=23&start=' + str(num)

    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    titles = soup.select('a.news_tit')

    for idx, title in enumerate(titles):
        title_txt = remove_tags(title.text)
        print(title_txt)

        label = 0
        pos_check = [s for s in positive if s in title_txt]
        neg_check = [s for s in negative if s in title_txt]

        # 긍정 체크
        if len(pos_check) > 0:
            label = -1
            print(">> positive match word : {0}, title : {1}".format(pos_check, title_txt))
        elif len(neg_check) > 0:
            label = 1
            print(">> positive match word : {0}, title : {1}".format(pos_check, title_txt))
        titles.append(title_txt)
        labels.append(label)

result_df = pd.DataFrame({'title': titles, 'label': labels})
result_df.to_csv('./../data/naver/이재명_라벨링.csv', encoding='utf-8-sig')