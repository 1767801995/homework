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

    work=soup.select('html')
    print(work)

    citys=[];adds=[];nows=[];cums=[];cures=[];deaths=[];

    for data in work:
        city = data.find_all("div",{"class":"VirusTable_1-1-265_AcDK7v"})
        city = city.find('span')[1].get_text(strip=True)
        citys.append(city)


        add=data.find("td",{"class":"VirusTable_1-1-265_3x1sDV VirusTable_1-1-265_2bK5NN"}).get_text(strip=True)
        adds.append(add)

        now=data.find("td",{"class":"VirusTable_1-1-265_3x1sDV"}).get_text(strip=True)
        nows.append(now)

        cum=data.find("td",{"class":"VirusTable_1-1-265_3x1sDV"}).get_text(strip=True)
        cums.append(cum)

        cure=data.find("td",{"class":"VirusTable_1-1-265_EjGi8c"}).get_text(strip=True)
        cures.append(cure)

        death = data.find("td", {"class": "VirusTable_1-1-265_EjGi8c"}).get_text(strip=True)
        deaths.append(death)

    print("citys:",citys)
    print("adds:",adds)
    print("nows:",nows)
    print("cums:",cums)
    print("cures:",cures)
    print("deaths:",deaths)
    return citys,adds,nows,cums,cures,deaths

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
    urls=['https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3#tab0']
    for url in urls:
        data=get_data(url)
        citys,adds,nows,cums,cures,deaths=parse_data(data)
