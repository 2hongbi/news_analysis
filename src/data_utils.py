import pandas as pd
import os.path


def extract_comments(file, output):
    df = pd.read_excel(file)
    if os.path.isfile(output):
        df.to_csv(output, sep=',', na_rep='NaN', columns=['내용'], index=False, mode='a', encoding='utf-8-sig',
                  header=False)
    else:
        df.to_csv(output, sep=',', na_rep='NaN', columns=['내용'], index=False, mode='w', encoding='utf-8-sig',
                  header=False)


if __name__ == '__main__':
    file_list = [
        '머니투데이_아프간난민을미군기지로.xlsx',
        'news1_아프간난민수용보도에찬반뜨거워.xlsx',
        '서울신문_전세계아프간난민딜레마.xlsx',
        '한겨레_한국협력한아프간현지인국내이송임박.xlsx',
        '한겨레_아프간피란민한국수용.xlsx',
        '한국일보_한국은선진국난민수용선택의문제아니다.xlsx'
    ]

    for file in file_list:
        extract_comments('./../data/'+file, './../data/comments.csv')