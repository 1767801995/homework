import work_data_china as ch
import work_data_world as wd
import work_data_US as us

if __name__=='__main__':
    url_wd='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    url_ch='https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=318268778643'
    url_us='http://m.sinovision.net/newpneumonia.php'
    input = input("请输入:'china' or 'world' or 'US'")
    if input=='china':
        print("开始爬取china数据")
        url=url_ch
        resp = ch.get_data(url)
        name, confirm, confirm_all, dead, heal = ch.parse_data(resp)
        ch.plt_data(name, confirm_all)
        ch.save_csv(name, confirm, confirm_all, dead, heal)
    elif input=='world':
        print("开始爬取world数据")
        url=url_wd
        resp = wd.get_data(url)
        name, confirm, confirm_all, heal, dead = wd.parse_data(resp)
        wd.save_csv(name, confirm, confirm_all, heal, dead)
    elif input=='US':
        print("开始爬取美国数据")
        url=url_us
        data = us.get_data(url)
        citys, cums, deaths = us.parse_data(data)
        us.dataview(citys, cums)
        us.save_data(citys, cums, deaths)
