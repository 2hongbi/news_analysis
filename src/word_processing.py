import pandas as pd
import re
# https://github.com/ssut/py-hanspell  https://hasiki.tistory.com/71 참고
from src.data_utils import hanspell_checking


def cleansing(text):
    # 이메일 주소 제거
    pattern = '(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\]+,\[a-zA-Z0-9-.\]+)'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # url 제거
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # 한글 자음, 모음 제거
    pattern = '([ㄱ-ㅎㅏ-ㅣ])+'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # html tag 제거
    pattern = '<[^>]*>'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # \r, \n 제거
    pattern = '[\r|\n]'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # 특수기호 제거
    pattern = '[^\w\s]'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # 이중 space 제거
    pattern = re.compile(r'\s+')
    text = re.sub(pattern=pattern, repl=' ', string=text)

    # emoji 제거
    pattern = re.compile("["
                         u"\U0001F600-\U0001F64F"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         "]+", flags=re.UNICODE)
    text = pattern.sub(r'', text)
    text = hanspell_checking(text)

    return text


if __name__ == '__main__':

    df = pd.read_csv('../data/all_nanmin_comments_with_likes.csv')
    df['comment'] = df['comment'].apply(cleansing)
    df.to_csv('./../data/cleansing/after_cleansing_with_likes.csv', sep=',', na_rep='NaN', encoding='utf-8-sig')