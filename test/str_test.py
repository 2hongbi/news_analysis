from itertools import product

candidate = ['이재명', '윤석열', '안철수', '심상정']
part = ['부동산', '경제', '외교/안보', '권력기관개혁', '청년문제']

result = [" ".join(i) for i in product(candidate, part)]
print(result, len(result))