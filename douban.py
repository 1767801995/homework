import requests
from bs4 import BeautifulSoup
import pandas as pd

#请求数据
def get_data(url):
    headers_value={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        data=requests.get(url,headers=headers_value)
    except requests.exceptions.ConnectionError as e:
        print("请求错误,url=",url)
        print("请求错误,",e)
        data=None
    return data
    #print(data.text)
#请求数据

#提取数据
def parse_data(data):
    soup=BeautifulSoup(data.text,'lxml')

    books_left=soup.find('ul',{'class':"cover-col-4 clearfix"})
    books_left=books_left.find_all("li")

    books_right=soup.find('ul',{'class':"cover-col-4 pl20 clearfix"})
    books_right=books_right.find_all("li")

    books=list(books_left)+list(books_right)

    img_urls=[];titles=[];ratings=[];authors=[];details=[];

    for book in books:
        img_url=book.find_all('a')[0].find('img').get('src')
        img_urls.append(img_url)

        title=book.find_all('a')[1].get_text()
        titles.append(title)

        rating=book.find('p',{'class':'rating'}).get_text()
        rating=rating.replace('\n','').replace(' ','')
        ratings.append(rating)

        detail=book.find_all('p')[2].get_text()
        detail = detail.replace('\n', '').replace(' ', '')
        details.append(detail)

        author=book.find('p',{'class':'color-gray'}).get_text(strip=True)
        #author=author.replace('\n', '').replace(' ', '')
        authors.append(author)

    print("img_urls:",img_urls)
    print("titles:",titles)
    print("details:",details)
    print("authors:",authors)
    print("ratings:",ratings)
    return img_urls,titles,details,authors,ratings
#提取数据

#数据存储
def save_data(img_urls,titles,details,authors,ratings):
    result=pd.DataFrame()
    result['img_url']=img_urls
    result['titles']=titles
    result['details']=details
    result['authors']=authors
    result['ratings']=ratings
    result.to_csv("D:/result.csv",encoding='utf_8_sig',index=None)
#数据存储

#网络爬虫
if __name__=='__main__':
    urls=['https://book.douban.com/latest']
    for url in urls:
        data=get_data(url)
        img_urls,titles,details,authors,ratings=parse_data(data)
    save_data(img_urls,titles,details,authors,ratings)
#网络爬虫