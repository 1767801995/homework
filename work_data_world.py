import requests
import json
import jsonpath
import pandas as pd
import requests
from pyecharts import options as opts
from pyecharts.charts import Map


#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        resp=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误",e)
        resp=None
    print("world数据请求成功")
    return resp

#爬取数据
def parse_data(resp):
        data=json.loads(resp.text)
        name=jsonpath.jsonpath(data, "$..name")
        confirm=jsonpath.jsonpath(data, "$..nowConfirm")
        confirm_all = jsonpath.jsonpath(data, "$..confirm")
        dead = jsonpath.jsonpath(data, "$..dead")
        heal = jsonpath.jsonpath(data, "$..heal")
        print("world 数据爬取成功！")
        print("国家:", name)
        print("现存确诊:", confirm)
        print("累计确诊:", confirm_all)
        print("死亡:", dead)
        print("治愈:", heal)
        return name,confirm,confirm_all,heal,dead

#数据储存csv
def save_csv(name,confirm,confirm_all,dead,heal):
    result=pd.DataFrame()
    result['国家']=name
    result['现有确诊']=confirm
    result['累计确诊']=confirm_all
    result['死亡']=dead
    result['治愈']=heal
    result.to_csv("data_world.csv", encoding='utf_8_sig', index=None)
    print("world数据保存csv成功，文件名：data_world.csv")


if __name__=='__main__':
    print("开始爬取world数据")
    url='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    resp=get_data(url)
    name, confirm, confirm_all, heal, dead = parse_data(resp)
    save_csv(name, confirm, confirm_all, heal, dead)
