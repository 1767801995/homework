# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 20:58
# @Author  : python_HongHu
# @Email   : 464646939@qq.com
# @File    : work_data_wcd.py
# @Software: PyCharm

import jieba
import requests
import json
import jsonpath
import pandas as pd
import matplotlib.pyplot as plt

#请求词云数据
def get_wcd(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        resp=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误", e)
        resp = None
    print("热点请求成功")

    return resp

#获取词云数据
def parse_data(resp):
    data = json.loads(resp.text)
    print(data)
    title = jsonpath.jsonpath(data, "$..title")
    print(title)
    print("词云热点数据爬取成功！")
    return title

#数据保存到CSV
def save_csv(title):
    result=pd.DataFrame()
    result['热点']=title
    result.to_csv("csv/热点.csv", encoding='utf_8_sig',index=None)

#读取csv文件
def read_wcd():
    df=pd.read_csv('csv/热点.csv')
    wordcloud=df['热点'].tolist()
    return wordcloud


if __name__=='__main__':
    url='https://api.dreamreader.qq.com/news/v1/province/news/list?province_code=bj&page_size=10'
    resp=get_wcd(url)
    title=parse_data(resp)
    save_csv(title)
    wordcloud=read_wcd()
