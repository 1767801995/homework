# -*- coding: utf-8 -*-
# @Time : 2021/3/10 14:49 
# @Author : python_HongHu
# @Email   : 1767801995@qq.com
# @File : in_data.py 
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
        resp=requests.get(url,headers=headers_value).json()
    except requests.exceptions.ConnectionError as e:
        print("请求错误,url=",url)
        print("请求错误,",e)
    print("国内总数据数据请求成功")
    print(resp)
    return resp

#提取数据
def parse_data(resp):
    data = json.loads(resp['data'])

    nowConfirm = data['chinaTotal']['nowConfirm']                   # 现有确诊
    nowConfirmAdd = data['chinaAdd']['nowConfirm']                  # 较上日新增现有确诊
    confirm = data['chinaTotal']['confirm']                         # 累计确诊
    confirmAdd = data['chinaAdd']['confirm']                        # 较上日新增累计确诊治愈
    heal = data['chinaTotal']['heal']                               # 累计治愈
    healAdd = data['chinaAdd']['heal']                              # 较上日新增累计治愈
    dead = data['chinaTotal']['dead']                               # 累计死亡
    deadAdd = data['chinaAdd']['dead']                              # 较上日新增累计死亡
    noInfect = data['chinaTotal']['noInfect']                       # 无症状感染者
    noInfectAdd = data['chinaAdd']['noInfect']                      # 较上日新增无症状感染者
    importedCase = data['chinaTotal']['importedCase']               # 境外输入
    importedCaseAdd = data['chinaAdd']['importedCase']              # 较上日新增境外输入
    suspect = data['chinaTotal']['suspect']                         # 现有疑似
    suspectAdd = data['chinaAdd']['suspect']                        # 较上日新增疑似
    localConfirm = data['chinaTotal']['localConfirm']               # 本土现有确诊
    localConfirmAdd = data['chinaAdd']['localConfirm']              # 较上日新增本土现有确诊
    lastUpdateTime = data['lastUpdateTime']                         # 数据更新时间


    return nowConfirm,nowConfirmAdd,confirm,confirmAdd,heal,healAdd,dead,deadAdd,\
           noInfect,noInfectAdd,importedCase,importedCaseAdd,suspect,suspectAdd,\
           localConfirm,localConfirmAdd,lastUpdateTime

# 数据存储到csv
def save_data(nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd,noInfect, noInfectAdd, importedCase, importedCaseAdd, suspect, suspectAdd,localConfirm, localConfirmAdd, lastUpdateTime):
    f = open('csv/in_data.csv', 'w', encoding='utf-8',newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(["nowConfirm", "nowConfirmAdd", "confirm", "confirmAdd", "heal", "healAdd", "dead", "deadAdd","noInfect", "noInfectAdd", "importedCase", "importedCaseAdd", "suspect", "suspectAdd","localConfirm", "localConfirmAdd", "lastUpdateTime"])
    csv_writer.writerow([nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd,noInfect, noInfectAdd, importedCase, importedCaseAdd, suspect, suspectAdd,localConfirm, localConfirmAdd, lastUpdateTime])
    print("国内数据保存csv成功，文件名：in_data.csv")

#数据存入mysql
def save_sql():
    data=pd.read_csv('csv/in_data.csv')
    rows_nums=data.shape[0]
    db=pymysql.connect(host='localhost',user='root',password='123456',db='android',charset='utf8')
    cursor=db.cursor()
    try:
        cursor.execute("drop table if exists in_data")
        cursor.execute("CREATE TABLE in_data("
                       "nowConfirm VARCHAR (100), "
                       "nowConfirmAdd VARCHAR (100),"
                       "confirm VARCHAR (100),"
                       "confirmAdd VARCHAR (100), "
                       "heal VARCHAR (100),"
                       "healAdd VARCHAR (100),"
                       "dead VARCHAR (100), "
                       "deadAdd VARCHAR (100),"
                       "noInfect VARCHAR (100),"
                       "noInfectAdd VARCHAR (100),"
                       "importedCase VARCHAR (100),"
                       "importedCaseAdd VARCHAR (100), "
                       "suspect VARCHAR (100),"
                       "suspectAdd VARCHAR (100),"
                       "localConfirm VARCHAR (100),"
                       "localConfirmAdd VARCHAR (100),"
                       "lastUpdateTime VARCHAR (200));")

        for i in range(rows_nums):
            sql = "INSERT INTO in_data(nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd,noInfect, noInfectAdd, importedCase, importedCaseAdd, suspect, suspectAdd,localConfirm, localConfirmAdd, lastUpdateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, (
                (str)(data.iloc[i, 0]), (str)(data.iloc[i, 1]), (str)(data.iloc[i, 2]),
                (str)(data.iloc[i, 3]),(str)(data.iloc[i, 4]),(str)(data.iloc[i, 5]),
                (str)(data.iloc[i, 6]),(str)(data.iloc[i, 7]),(str)(data.iloc[i, 8]),
                (str)(data.iloc[i, 9]),(str)(data.iloc[i, 10]),(str)(data.iloc[i, 11]),
                (str)(data.iloc[i, 12]),(str)(data.iloc[i, 13]),(str)(data.iloc[i, 14]),
                (str)(data.iloc[i, 15]),(str)(data.iloc[i, 16])))
        cursor.close()
        db.commit()
        print("国内数据保存已保存到mysql")
    except :
        db.rollback()
        print("ERROR")
        cursor.close()
    finally:
        cursor.close()



if __name__== '__main__':
    # url="https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=323073930260"   #163
    url="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    resp=get_data(url)
    nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd,noInfect, noInfectAdd, importedCase, importedCaseAdd, suspect, suspectAdd,localConfirm, localConfirmAdd, lastUpdateTime=parse_data(resp)
    save_data(nowConfirm, nowConfirmAdd, confirm, confirmAdd, heal, healAdd, dead, deadAdd,noInfect, noInfectAdd, importedCase, importedCaseAdd, suspect, suspectAdd,localConfirm, localConfirmAdd, lastUpdateTime)
    save_sql()



