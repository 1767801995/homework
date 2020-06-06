import json
import jsonpath
import pandas as pd
import requests
from pyecharts import options as opts
from pyecharts.charts import Map
import matplotlib.pyplot as plt
from pyecharts.faker import Faker

#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        resp=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误",e)
        resp=None
    print("china数据请求成功")
    return resp

#爬取数据
def parse_data(resp):
        print(resp.text)
        data=json.loads(resp.text)
        name=jsonpath.jsonpath(data,"$.data.areaTree[2].children[*].name")                  #省份名
        confirm=jsonpath.jsonpath(data,"$.data.areaTree[2].children[*].today.confirm")      #现有确诊
        confirm_all=jsonpath.jsonpath(data,"$.data.areaTree[2].children[*].total.confirm")  #累计确诊
        dead = jsonpath.jsonpath(data, "$.data.areaTree[2].children[*].total.dead")         #累计死亡
        heal=jsonpath.jsonpath(data,"$.data.areaTree[2].children[*].total.heal")            #累计确诊
        print("china 数据爬取成功！")
        print("name:",name)
        print("confirm:",confirm)
        print("confirm_all:",confirm_all)
        print("dead:",dead)
        print("heal:",heal)
        return name,confirm,confirm_all,dead,heal

#数据储存csv
def save_csv(name,confirm,confirm_all,dead,heal):
    result=pd.DataFrame()
    result['省份']=name
    result['新增确诊']=confirm
    result['累计确诊']=confirm_all
    result['死亡']=dead
    result['治愈']=heal
    result.to_csv("data_china.csv", encoding='utf_8_sig', index=None)
    print("中国数据保存csv成功，文件名：data_china.csv")

#PyechartsMap 地图
def plt_data(name,confirm_all):
    data_list=zip(name,confirm_all)
    map = Map().add(series_name='累计确诊',
                  data_pair=data_list,
                  maptype="china",
                  is_map_symbol_show=False)
    map.set_series_opts(label_opts=opts.LabelOpts(is_show=True))  # 关闭省份名称显示
    map.set_global_opts(title_opts=opts.TitleOpts("中国疫情"), visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color,max_=1000) ) # 图例显示
    map.render("中国疫情分布图.html")
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.bar(range(len(confirm_all)), confirm_all, tick_label=name)
    plt.xticks(rotation=270)
    plt.savefig("中国疫情柱状图")
    print("中国数据可视化成功，文件名：中国疫情分布图.html、中国疫情柱状图.png")


#数据存入xlsx


if __name__=='__main__':
    url="https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318268778643"
    resp=get_data(url)
    name,confirm,confirm_all,dead,heal=parse_data(resp)
    plt_data(name,confirm_all)
    save_csv(name,confirm,confirm_all,dead,heal)