import pymysql
import requests
import json
import jsonpath
import pandas as pd
import requests
from pyecharts import options as opts
from pyecharts.charts import Map


#请求数据
from pyecharts.faker import Faker


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

#数据存入mysql
def save_sql():
    data=pd.read_csv('data_world.csv')
    rows_nums=data.shape[0]
    db=pymysql.connect(host='localhost',user='root',password='123456',db='python',charset='utf8')
    cursor=db.cursor()
    try:
        cursor.execute("drop table if exists data_world")
        cursor.execute("CREATE TABLE data_world("
                       "name VARCHAR (100), "
                       "confirm VARCHAR (100),"
                       "confirm_all VARCHAR (100),"
                       "dead VARCHAR (100),"
                       "heal VARCHAR (200));")
        for i in range(rows_nums):
            sql = "INSERT INTO data_world(name, confirm,confirm_all,dead,heal) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql, (
                (str)(data.iloc[i, 0]), (str)(data.iloc[i, 1]), (str)(data.iloc[i, 2]), (str)(data.iloc[i, 3]),
                (str)(data.iloc[i, 4])))
        cursor.close()
        db.commit()
        print("世界疫情数据保存已保存到mysql")
    except:
        db.rollback()
        print("ERROR")
        cursor.close()
    finally:
        cursor.close()

#可视化
def plt_data(name,confirm_all):
    nameMap = {
        'Singapore Rep.': '新加坡',
        'Dominican Rep.': '多米尼加',
        'Palestine': '巴勒斯坦',
        'Bahamas': '巴哈马',
        'Timor-Leste': '东帝汶',
        'Afghanistan': '阿富汗',
        'Guinea-Bissau': '几内亚比绍',
        "Côte d'Ivoire": '科特迪瓦',
        'Siachen Glacier': '锡亚琴冰川',
        "Br. Indian Ocean Ter.": '英属印度洋领土',
        'Angola': '安哥拉',
        'Albania': '阿尔巴尼亚',
        'United Arab Emirates': '阿联酋',
        'Argentina': '阿根廷',
        'Armenia': '亚美尼亚',
        'French Southern and Antarctic Lands': '法属南半球和南极领地',
        'Australia': '澳大利亚',
        'Austria': '奥地利',
        'Azerbaijan': '阿塞拜疆',
        'Burundi': '布隆迪',
        'Belgium': '比利时',
        'Benin': '贝宁',
        'Burkina Faso': '布基纳法索',
        'Bangladesh': '孟加拉国',
        'Bulgaria': '保加利亚',
        'The Bahamas': '巴哈马',
        'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
        'Belarus': '白俄罗斯',
        'Belize': '伯利兹',
        'Bermuda': '百慕大',
        'Bolivia': '玻利维亚',
        'Brazil': '巴西',
        'Brunei': '文莱',
        'Bhutan': '不丹',
        'Botswana': '博茨瓦纳',
        'Central African Rep.': '中非共和国',
        'Canada': '加拿大',
        'Switzerland': '瑞士',
        'Chile': '智利',
        'China': '中国',
        'Ivory Coast': '象牙海岸',
        'Cameroon': '喀麦隆',
        'Dem. Rep. Congo': '刚果（金）',
        'Congo': '刚果（布）',
        'Colombia': '哥伦比亚',
        'Costa Rica': '哥斯达黎加',
        'Cuba': '古巴',
        'N. Cyprus': '北塞浦路斯',
        'Cyprus': '塞浦路斯',
        'Czech Rep.': '捷克',
        'Germany': '德国',
        'Djibouti': '吉布提',
        'Denmark': '丹麦',
        'Algeria': '阿尔及利亚',
        'Ecuador': '厄瓜多尔',
        'Egypt': '埃及',
        'Eritrea': '厄立特里亚',
        'Spain': '西班牙',
        'Estonia': '爱沙尼亚',
        'Ethiopia': '埃塞俄比亚',
        'Finland': '芬兰',
        'Fiji': '斐',
        'Falkland Islands': '福克兰群岛',
        'France': '法国',
        'Gabon': '加蓬',
        'United Kingdom': '英国',
        'Georgia': '格鲁吉亚',
        'Ghana': '加纳',
        'Guinea': '几内亚',
        'Gambia': '冈比亚',
        'Guinea Bissau': '几内亚比绍',
        'Eq. Guinea': '赤道几内亚',
        'Greece': '希腊',
        'Greenland': '格陵兰',
        'Guatemala': '危地马拉',
        'French Guiana': '法属圭亚那',
        'Guyana': '圭亚那',
        'Honduras': '洪都拉斯',
        'Croatia': '克罗地亚',
        'Haiti': '海地',
        'Hungary': '匈牙利',
        'Indonesia': '印度尼西亚',
        'India': '印度',
        'Ireland': '爱尔兰',
        'Iran': '伊朗',
        'Iraq': '伊拉克',
        'Iceland': '冰岛',
        'Israel': '以色列',
        'Italy': '意大利',
        'Jamaica': '牙买加',
        'Jordan': '约旦',
        'Japan': '日本',
        'Japan': '日本本土',
        'Kazakhstan': '哈萨克斯坦',
        'Kenya': '肯尼亚',
        'Kyrgyzstan': '吉尔吉斯斯坦',
        'Cambodia': '柬埔寨',
        'Korea': '韩国',
        'Kosovo': '科索沃',
        'Kuwait': '科威特',
        'Lao PDR': '老挝',
        'Lebanon': '黎巴嫩',
        'Liberia': '利比里亚',
        'Libya': '利比亚',
        'Sri Lanka': '斯里兰卡',
        'Lesotho': '莱索托',
        'Lithuania': '立陶宛',
        'Luxembourg': '卢森堡',
        'Latvia': '拉脱维亚',
        'Morocco': '摩洛哥',
        'Moldova': '摩尔多瓦',
        'Madagascar': '马达加斯加',
        'Mexico': '墨西哥',
        'Macedonia': '马其顿',
        'Mali': '马里',
        'Myanmar': '缅甸',
        'Montenegro': '黑山',
        'Mongolia': '蒙古',
        'Mozambique': '莫桑比克',
        'Mauritania': '毛里塔尼亚',
        'Malawi': '马拉维',
        'Malaysia': '马来西亚',
        'Namibia': '纳米比亚',
        'New Caledonia': '新喀里多尼亚',
        'Niger': '尼日尔',
        'Nigeria': '尼日利亚',
        'Nicaragua': '尼加拉瓜',
        'Netherlands': '荷兰',
        'Norway': '挪威',
        'Nepal': '尼泊尔',
        'New Zealand': '新西兰',
        'Oman': '阿曼',
        'Pakistan': '巴基斯坦',
        'Panama': '巴拿马',
        'Peru': '秘鲁',
        'Philippines': '菲律宾',
        'Papua New Guinea': '巴布亚新几内亚',
        'Poland': '波兰',
        'Puerto Rico': '波多黎各',
        'Dem. Rep. Korea': '朝鲜',
        'Portugal': '葡萄牙',
        'Paraguay': '巴拉圭',
        'Qatar': '卡塔尔',
        'Romania': '罗马尼亚',
        'Russia': '俄罗斯',
        'Rwanda': '卢旺达',
        'W. Sahara': '西撒哈拉',
        'Saudi Arabia': '沙特阿拉伯',
        'Sudan': '苏丹',
        'S. Sudan': '南苏丹',
        'Senegal': '塞内加尔',
        'Solomon Is.': '所罗门群岛',
        'Sierra Leone': '塞拉利昂',
        'El Salvador': '萨尔瓦多',
        'Somaliland': '索马里兰',
        'Somalia': '索马里',
        'Serbia': '塞尔维亚',
        'Suriname': '苏里南',
        'Slovakia': '斯洛伐克',
        'Slovenia': '斯洛文尼亚',
        'Sweden': '瑞典',
        'Swaziland': '斯威士兰',
        'Syria': '叙利亚',
        'Chad': '乍得',
        'Togo': '多哥',
        'Thailand': '泰国',
        'Tajikistan': '塔吉克斯坦',
        'Turkmenistan': '土库曼斯坦',
        'East Timor': '东帝汶',
        'Trinidad and Tobago': '特里尼达和多巴哥',
        'Tunisia': '突尼斯',
        'Turkey': '土耳其',
        'Tanzania': '坦桑尼亚',
        'Uganda': '乌干达',
        'Ukraine': '乌克兰',
        'Uruguay': '乌拉圭',
        'United States': '美国',
        'Uzbekistan': '乌兹别克斯坦',
        'Venezuela': '委内瑞拉',
        'Vietnam': '越南',
        'Vanuatu': '瓦努阿图',
        'West Bank': '西岸',
        'Yemen': '也门',
        'South Africa': '南非',
        'Zambia': '赞比亚',
        'Zimbabwe': '津巴布韦'
    }
    data_list=zip(name,confirm_all)
    map = Map(opts.InitOpts(width='1600px',height='600px')).add(series_name='确诊人数',
                  data_pair=data_list,
                  maptype="world",
                  name_map=nameMap,
                  is_map_symbol_show=False)
    map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 关闭国家名称显示
    map.set_global_opts(title_opts=opts.TitleOpts("世界疫情"),
                        visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color, max_=70000))  # 图例显示
    map.render("html/世界疫情分布图.html")
    print("世界数据可视化成功，文件名：世界疫情分布图.html")


if __name__=='__main__':
    print("开始爬取world数据")
    url='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
    resp=get_data(url)
    name, confirm, confirm_all, heal, dead = parse_data(resp)
    save_csv(name, confirm, confirm_all, heal, dead)
    plt_data(name,confirm_all)
    save_sql()
