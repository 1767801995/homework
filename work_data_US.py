import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.datasets import register_url
from pyecharts.faker import Faker

#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        data=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误,url=",url)
        print("请求错误,",e)
        data=None
    print("美国数据请求成功")
    return data

#提取数据
def parse_data(data):
    soup=BeautifulSoup(data.text,'lxml')

    work=soup.find_all("div",{'class':"todaydata"})[2]
    work=work.find_all("div")
    work=list(work)
    citys=[];cums=[];deaths=[];
    for data in work:
        city = data.find("div",{'class':"prod tags"})
        if (city!=None):
            city = city.find("span",{'class':"area"}).get_text()
            citys.append(city)

        cum = data.find("div", {'class': "prod tags"})
        if (cum != None):
            cum = cum.find("span", {'class': "confirm"}).get_text()
            cums.append(cum)

        death = data.find("div", {'class': "prod tags"})
        if (death != None):
            death= death.find("span", {'class': "dead"}).get_text()
            deaths.append(death)
        #数据处理
        for i in range(len(citys)):
            if cums[i]==None:
                cums[i]=0
            elif deaths[i]==None:
                deaths[i]=0
    print("美国数据爬取成功")
    print("州名称:",citys)
    print("确诊:",cums)
    print("死亡:",deaths)
    return citys,cums,deaths

#数据存储到csv
def save_data(citys,cums,deaths):
    result=pd.DataFrame()
    result['citys']=citys
    result['cums']=cums
    result['deaths']=deaths
    result.to_csv("csv/data_US.csv",encoding='utf_8_sig',index=None)
    print("美国数据保存csv成功，文件名：data_US.csv")

#数据存入mysql
def save_sql():
    data=pd.read_csv('csv/data_US.csv')
    rows_nums=data.shape[0]
    db=pymysql.connect(host='localhost',user='root',password='123456',db='python',charset='utf8')
    cursor=db.cursor()
    try:
        cursor.execute("drop table if exists data_us")
        cursor.execute("CREATE TABLE data_us("
                       "citys VARCHAR (100), "
                       "cums VARCHAR (100),"
                       "deaths VARCHAR (200));")
        for i in range(rows_nums):
            sql = "INSERT INTO data_us(citys, cums,deaths) VALUES (%s,%s,%s);"
            cursor.execute(sql, (
                (str)(data.iloc[i, 0]), (str)(data.iloc[i, 1]), (str)(data.iloc[i, 2])))
        cursor.close()
        db.commit()
        print("美国数据保存已保存到mysql")
    except:
        db.rollback()
        print("ERROR")
        cursor.close()
    finally:
        cursor.close()

#可视化
def plt_data(citys,cums):
    register_url("https://echarts-maps.github.io/echarts-countries-js/")
    data_list=zip(citys,cums)
    map=Map(opts.InitOpts(width='1600px',height='600px')).add(series_name='确诊人数',
                  data_pair=data_list,
                  maptype="美国",
                  is_map_symbol_show=False,
                  )
    map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #关闭名称显示
    map.set_global_opts(title_opts=opts.TitleOpts("美国疫情"),
                        visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color,max_=10000),
                        )
    map.render("html/美国疫情分布图.html")
    print("美国数据可视化成功，文件名：美国疫情分布图.html")


#网络爬虫
if __name__=='__main__':
    print("开始爬取美国数据")
    url='http://m.sinovision.net/newpneumonia.php'
    data=get_data(url)
    citys,cums,deaths=parse_data(data)
    plt_data(citys, cums)
    save_data(citys,cums,deaths)
    save_sql()
