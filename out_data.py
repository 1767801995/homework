# -*- coding: utf-8 -*-
# @Time : 2021/3/8 14:47 
# @Author : python_HongHu
# @Email   : 1767801995@qq.com
# @File : out_data.py 
# @Software: PyCharm

import json
import csv
import pymysql
import jsonpath
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.datasets import register_url
from pyecharts.faker import Faker

#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    try:
        # url='https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd'
        resp=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误,url=",url)
        print("请求错误,",e)
        data=None
    print("美国数据请求成功")
    return resp

#提取数据
def parse_data(resp):
    data=json.loads(resp.text)
    nowConfirm =data['data']['FAutoGlobalStatis']['nowConfirm']         #现有确诊
    nowConfirmAdd =data['data']['FAutoGlobalStatis']['nowConfirmAdd']   #较上日新增现有确诊
    confirm = data['data']['FAutoGlobalStatis']['confirm']              #累计确诊
    confirmAdd = data['data']['FAutoGlobalStatis']['confirmAdd']        #较上日新增累计确诊
    heal = data['data']['FAutoGlobalStatis']['heal']                    #累计治愈
    healAdd = data['data']['FAutoGlobalStatis']['healAdd']              #较上日新增累计治愈
    dead = data['data']['FAutoGlobalStatis']['dead']                    #累计死亡
    deadAdd = data['data']['FAutoGlobalStatis']['deadAdd']              #较上日新增累计累计死亡
    lastUpdateTime = data['data']['FAutoGlobalStatis']['lastUpdateTime']    #数据更新时间
    print(nowConfirm)
    print(nowConfirmAdd)
    print(confirm)
    print(confirmAdd)
    print(heal)
    print(healAdd)
    print(dead)
    print(deadAdd)
    print(lastUpdateTime)

    return nowConfirm, nowConfirmAdd, confirm,confirmAdd,heal,healAdd,dead,deadAdd,lastUpdateTime

# 数据存储到csv
def save_data(nowConfirm, nowConfirmAdd, confirm,confirmAdd,heal,healAdd,dead,deadAdd,lastUpdateTime):
    f = open('csv/out_data.csv', 'w', encoding='utf-8',newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(["nowConfirm", "nowConfirmAdd", "confirm","confirmAdd", "heal", "healAdd","dead", "deadAdd", "lastUpdateTime"])
    csv_writer.writerow([nowConfirm, nowConfirmAdd, confirm,confirmAdd,heal,healAdd,dead,deadAdd,lastUpdateTime])
    print("国外数据保存csv成功，文件名：out_data.csv")


#数据存入mysql
def save_sql():
    data=pd.read_csv('csv/out_data.csv')
    rows_nums=data.shape[0]
    db=pymysql.connect(host='localhost',user='root',password='123456',db='android',charset='utf8')
    cursor=db.cursor()
    try:
        cursor.execute("drop table if exists out_data")
        cursor.execute("CREATE TABLE out_data("
                       "nowConfirm VARCHAR (100), "
                       "nowConfirmAdd VARCHAR (100),"
                       "confirm VARCHAR (200),"
                       "confirmAdd VARCHAR (100), "
                       "heal VARCHAR (100),"
                       "healAdd VARCHAR (200),"
                       "dead VARCHAR (100), "
                       "deadAdd VARCHAR (100),"
                       "lastUpdateTime VARCHAR (200));")
        for i in range(rows_nums):
            sql = "INSERT INTO out_data(nowConfirm, nowConfirmAdd, confirm,confirmAdd,heal,healAdd,dead,deadAdd,lastUpdateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, (
                (str)(data.iloc[i, 0]), (str)(data.iloc[i, 1]), (str)(data.iloc[i, 2]),
                (str)(data.iloc[i, 3]),(str)(data.iloc[i, 4]),(str)(data.iloc[i, 5]),
                (str)(data.iloc[i, 6]),(str)(data.iloc[i, 7]),(str)(data.iloc[i, 8])))
        cursor.close()
        db.commit()
        print("国外数据保存已保存到mysql")
    except :
        db.rollback()
        print("ERROR")
        cursor.close()
    finally:
        cursor.close()



if __name__== '__main__':
    url="https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd"
    resp=get_data(url)
    nowConfirm, nowConfirmAdd, confirm,confirmAdd,heal,healAdd,dead,deadAdd,lastUpdateTime =parse_data(resp)
    save_data(nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd, lastUpdateTime)
    save_sql()

