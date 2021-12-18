from itertools import product

import tqdm.notebook
import twint


def grab_tweets(search, file, since):
    c = twint.Config()
    c.Search = search
    c.Since = since
    c.Hide_output = True
    c.Store_json = True
    c.Output = file
    twint.run.Search(c)


if __name__ == '__main__':

    candidate = ['안철수', '심상정']
    # part = ['부동산', '경제', '외교안보', '권력기관개혁', '청년문제']

    # result = [" ".join(i) for i in product(candidate, part)]
    # print(result, len(result)

    for q in tqdm.notebook.tqdm(candidate):
        print('>> ' + q)
        try:
            grab_tweets(q, './../data/twitter/'+q+'.json', '2021-11-10')

            df = pd.read_json('./../data/twitter/'+q+'.json', lines=True)
            df['tweet'] = df['tweet'].apply(cleansing)

            new_df = df.filter(['tweet', 'date', 'retweets_count', 'likes_count', 'link'], axis=1)
            new_df.to_csv('./../data/twitter/'+q+'.csv', encoding='utf-8-sig', index=False)
        except ValueError:
            print('>>> Value Error: '+q)
            pass
        except TypeError:
            print('>>> Type Error: '+q)



