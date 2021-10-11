import pandas as pd
import re
from konlpy.tag import Okt
from collections import Counter
from ckonlpy.tag import Twitter

print("엑셀파일 데이터프레임으로 불러오기")
# \한개만 붙이면 제대로 실행 안 될 수도 있음. \\쓰는 걸 권장
# 상대경로 자꾸 에러 나서 절대경로로 지정함.
data = pd.read_excel("c:\\Users\\LG\\Desktop\\OUTLIER\\OUTLIER_7조\\article\\news1_아프간난민수용보도에찬반뜨거워.xlsx")
df = pd.DataFrame(data)
del df['Unnamed: 0']  # 댓글 순서 나타내는 열 중복되서 하나 지움.
print(df)

print("형태소 추출을 위한 준비과정 (re, Okt이용)")
print("\n준비과정 1 - 댓글들 한줄로 만들기")
# 문자열을 리스트 형태가 아닌 따옴표로 만들기 -> 댓글이 하나의 문장처럼 쭉 이어짐.
# for문에 range를 사용해서 댓글 개수만큼 반복하도록 설정
content_all = ''
for i in range(len(df['내용'])):
    content_all = content_all + ' ' + df['내용'].loc[i]
print(content_all)

print("\n준비과정 2 - 정규화(normalization) 처리")
# Okt의 normalize()를 이용해서 정규화 처리하기
# 단어의 개수를 줄일 수 있어서 자연어 처리 성능을 얻을 수 있음.
# ex) '안녕하세욬ㅋㅋㅋㅋ 사릉해'를 정규화 처리하면 '안녕하세요ㅋㅋㅋ 사랑해'로 바뀜.
okt = Okt()
content_all = (okt.normalize(content_all))
print(content_all)

print("\n준비과정 3 - 한글, 숫자만 가능하도록 댓글 처리(영어, 특수문자 제거하기), 정규식으로 표현")
# re 라이브러리 이용해서 영어, 특수문자 등등 제거하기
# 아래 코드에서 문자형이 아니라 안된다는 에러 나면 content_all = str(content_all) 사용!
content_all = re.sub('[^ㄱ-ㅣ가-힣0-9]', " ", content_all)
print(content_all)

print("\n준비과정 4 - 명사 단위, 형태소 단위 등등으로 쪼개기")
# 형태소 추출도구로 konlpy의 Okt와 Twitter 사용해보기
# ckonlpy는 Customized Konlpy로 Konlpy의 customized version이라고 보면 된다.
# ++ 추가 UserWarning 메시지 내용 : KoNLPy 0.4.5 버전부터는 Twitter 패키지 이름이 Okt로 바꼈다. -> 에러는 안남. 편의상 코드에서는 Twitter로 표현하겠음!

print("\n명사 단위로 쪼개기")
# 명사 단위로 쪼개서 nouns_txt에 담기
# ++ 추가 ex) '절대 반대'를 '절대' + '반대'로 쪼개서 담는게 싫다면 Twitter 이용해서 임의로 명사 추가하기!('절대 반대'가 한 단어로 취급)

Twitter = Twitter()
Twitter.add_dictionary('아프간난민', 'Noun')
Twitter.add_dictionary('아프간 난민', 'Noun')

# Twitter의 add_dictionary()를 통해서 명사 추가하고, Okt를 통해 다시 한번 명사 쪼개면 해결!
nouns_txt = okt.nouns(content_all)
print(nouns_txt)

print("\n형태소 단위로 쪼개기")
morphs_txt = okt.morphs(content_all)
print(morphs_txt)

# 형태소와 품사를 추출
"""
pos_txt = okt.pos(content_all)
print(pos_txt)
"""

print("\n준비과정 5 - 명사, 형태소 몇번 언급되었는지 세기")
# from collections import Counter       <- jdk에서 제공하는 라이브러리 사용
# nouns_txt에서 nouns 개수 세어주는 Counter 이용
count_nouns = Counter(nouns_txt)      # 결과는 딕셔너리 형태와 비슷하게 표현됨.
count_morphs = Counter(morphs_txt)
rank_nouns_text = count_nouns.most_common()     # 내림차순 정렬
rank_morphs_text = count_morphs.most_common()
print(rank_nouns_text)
print(rank_morphs_text)

print("\n준비과정 6 - 불용어(전치사, 접속사, 조사 등), 중요하지 않은 단어들 제외하기(단어 한번 더 정제하는 과정)")
print("\n중요하지 않은 단어들 제외하기")
# 워드클라우드로 표현할 때 모든 단어 다 나타내기에는 양이 많기 때문에 단어들 한번 더 정제하기
# n번 미만으로 언급된 단어 제외하기
rank_text = dict(rank_nouns_text)     # rank_nouns_text를 딕셔너리 형태로 바꾸기
count_len = 10      # 'n번 미만으로 언급된 단어'에서 n 지정하기(단어 버리는 기준 숫자)
temp_dic = {}
for key, value in rank_text.items():        # .items() 써서 key값, value값 다 추출하기
    if value > count_len:
        temp_dic[key] = value
rank_text = temp_dic
print(rank_text)

print("\n불용어 제거하기")
# 방법 2가지 중 하나 택하기

# 방법 1 : 파일로 처리하기 - 사용자가 제외할 단어를 직접 추가하거나 제외할 수 있어서 편리함
# 큰 틀은 파일 다운 받아서 사용하고, 더 추가할 단어를 .append()하는 게 베스트
k_remove_word = pd.read_csv("../data/korean_stopword.csv")
k_remove_word = list(k_remove_word['불용어'])
k_remove_word.append('더 제외할 단어')

temp_dic = {}
for key, value in rank_text.items():
    if key not in k_remove_word:        # k_remove_word가 아닌 키값만 다시 모아서 딕셔너리 형태로 temp_dic에 반환
        temp_dic[key] = value
print(temp_dic)

# 방법 2 : 라이브러리 설치해서 처리하기

print("\n준비과정 7 - 단어 수작업으로 정제하기")
# 정제 과정 거쳐도 중요하지 않은 단어들 남아있을 수 있기 때문에 한번 더 수작업하기 -> 워드 클라우드가 더 깔끔해질 수 있음!
# [temp_dic.pop(key) for key in ['지우고 싶은 단어1', '지우고 싶은 단어2', ... , '지우고 싶은 단어n']]
[temp_dic.pop(key) for key in ['왜', '땅']]
print(temp_dic)

print("\n워드클라우드 그리기(WordCloud이용)")
