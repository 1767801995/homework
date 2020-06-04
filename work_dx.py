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

    work=soup.select('#root > div > div.mapBox___qoGhu > div:nth-child(10) > div.expand___LP7tG > div.areaBlock1___3qjL7 > p.subBlock1___3cWXy')
    print(work)

    citys=[];nows=[];cums=[];cures=[];deaths=[];

    for data in work:
        city = data.find_all('p')[0].get_text()
        citys.append(city)

        now=data.find("p",{"class":"subBlock2___2BONl"}).get_text()
        nows.append(now)

        cum=data.find("p",{"class":"subBlock3___3dTLM"}).get_text()
        cums.append(cum)

        cure=data.find("p",{"class":"subBlock5___33XVW"}).get_text()
        cures.append(cure)

        death = data.find("p", {"class": "subBlock4___3SAto"}).get_text()
        deaths.append(death)

    print("citys:",citys)
    print("nows:",nows)
    print("cums:",cums)
    print("cures:",cures)
    print("deaths:",deaths)
    return citys,nows,cums,cures,deaths





#数据存储
def save_data(img_urls,titles,details,authors,ratings):
    result=pd.DataFrame()
    result['img_url']=img_urls
    result['titles']=titles
    result['details']=details
    result['authors']=authors
    result['ratings']=ratings
    result.to_csv("D:/result.csv",encoding='utf_8_sig',index=None)


#网络爬虫
if __name__=='__main__':
    urls=['https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0']
    for url in urls:
        data=get_data(url)
        citys,nows,cums,cures,deaths=parse_data(data)
