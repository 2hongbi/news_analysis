import pandas as pd
import os

filePath = 'C://Users//foxgi//OneDrive//project//DWU//outlier//news_analysis//data//twitter//이재명.csv'  # 폴더 주소 입력

rowsize = sum(1 for row in (open(filePath, encoding='UTF-8')))
newsize = 50000   # 쪼개고 싶은 행수 수준으로 입력. 이정도 행수는 200mb 이하임.
times = 0
for i in range(1, rowsize, newsize):
    times += 1   # 폴더 내 파일을 하나씩 점검하면서, 입력한 newsize보다 넘는 행을 쪼개줌
    df = pd.read_csv(filePath, header=None, nrows = newsize, skiprows=i)
    csv_output = filePath[:-4] + '_' + str(times) + '.csv'   # 쪼갠 수만큼 _1, _2... _n으로 꼬리를 달아서 파일명이 저장됨
    df.to_csv(csv_output, index=False, header=False, mode='a', chunksize=rowsize, encoding='utf-8-sig')
    print(df)