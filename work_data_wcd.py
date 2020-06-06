import jieba
import requests
import json
import jsonpath
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from imageio import imread

def get_wcd(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        resp=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误", e)
        resp = None
    print("热点请求成功")

    return resp


def parse_data(resp):
    data = json.loads(resp.text)
    print(data)
    title = jsonpath.jsonpath(data, "$..title")
    print(title)
    print("world 数据爬取成功！")
    return title

def save_xlsx(title):
    result=pd.DataFrame()
    result['热点']=title
    result.to_csv("热点.csv", encoding='utf_8_sig',index=None)


def read_wcd():
    df=pd.read_csv('热点.csv')
    wordcloud=df['热点'].tolist()
    return wordcloud

def make_wcd(wordcloud):
    word_list=[" ".join(jieba.cut(sentence)) for sentence in wordcloud]
    new_text=' '.join(word_list)
    pic_path='1.jpg'
    img_mask=imread(pic_path)

    wordcloud = WordCloud(background_color="white", font_path='/home/shen/Downloads/font/msyh.ttc', mask=img_mask,
                          stopwords=STOPWORDS).generate(new_text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

if __name__=='__main__':
    url='https://api.dreamreader.qq.com/news/v1/province/news/list?province_code=hb&page_size=10'
    resp=get_wcd(url)
    title=parse_data(resp)
    save_xlsx(title)
    wordcloud=read_wcd()
    make_wcd(wordcloud)
