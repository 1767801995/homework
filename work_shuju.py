import requests
from bs4 import BeautifulSoup
import pandas as pd

#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        data=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误,url=",url)
        print("请求错误,",e)
        data=None
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

    print("citys:",citys)
    print("cums:",cums)
    print("deaths:",deaths)
    return citys,cums,deaths


#数据存储
def save_data(citys,cums,deaths):
    result=pd.DataFrame()
    result['citys']=citys
    result['cums']=cums
    result['deaths']=deaths
    result.to_csv("C:/Users/Administrator/PycharmProjects/homework/result.csv",encoding='utf_8_sig',index=None)


#网络爬虫
if __name__=='__main__':
    urls=['http://m.sinovision.net/newpneumonia.php']
    for url in urls:
        data=get_data(url)
        citys,cums,deaths=parse_data(data)
    save_data(citys,cums,deaths)
