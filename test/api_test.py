import requests
from consts import NAVER_API

# naver news api 호출
url = 'https://openapi.naver.com/v1/search/news.json'

# api 이용시 필요한 정보들 넘기는 작업
headers = {'X-Naver-Client-Id': NAVER_API['CLIENT_ID'], 'X-Naver-Client-Secret': NAVER_API['CLIENT_SECRET']}

# params의 query에서 키워드 수정하여 검색
params = {'query': '한국 아프간 난민 수용', 'sort': 'date'}
req = requests.get(url, params=params, headers=headers)

# 결과를 json 형식으로 받아옴
result = req.json()
print(result)
