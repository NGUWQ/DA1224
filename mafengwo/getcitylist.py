import requests
import pandas as pd
from lxml import etree
from selenium import webdriver
import re
import os

os.chdir('C:/爬虫/蚂蜂窝')

data=pd.read_excel('C:/爬虫/蚂蜂窝/国内热门目的地.xlsx')
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'cookie':'PHPSESSID=f3r2e17ar2sp3t32qa8mk4u283; mfw_uuid=5b812333-dca2-d3c8-b81e-8afd2e094be6; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A15%3A%22www.baidu.com%2Fs%22%3Bs%3A1%3A%22t%22%3Bi%3A1535189811%3B%7D; oad_n=a%3A6%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22wk%22%3Bs%3A12%3A%22%C2%EC%B7%E4%CE%D1%C2%C3%D3%CE%CD%F8%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A3546%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222018-08-25+17%3A36%3A51%22%3B%7D; uva=s%3A587%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222018-08-25%22%3Bs%3A2%3A%22lt%22%3Bi%3A1535189812%3Bs%3A10%3A%22last_refer%22%3Bs%3A460%3A%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E8%259A%2582%25E8%259C%2582%25E7%25AA%259D%25E6%2597%2585%25E6%25B8%25B8%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xfa1aedf500026e2a%26issp%3D1%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26oq%3Dexcel%2525E8%2525AE%2525BE%2525E7%2525BD%2525AE%2525E8%2525A1%25258C%2525E9%2525AB%252598%26rsv_t%3Ddb67QdWkzSaIRtELssTN97o%252BQyTItV6LIGwjdJoSTyfMbWVllXPgxkPqUafpxydWkTli%26inputT%3D7411%26rsv_pq%3Da9dee28900027aaa%26rsv_sug3%3D19%26rsv_sug1%3D17%26rsv_sug7%3D100%26bs%3Dexcel%25E8%25AE%25BE%25E7%25BD%25AE%25E8%25A1%258C%25E9%25AB%2598%22%3Bs%3A5%3A%22rhost%22%3Bs%3A13%3A%22www.baidu.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1535189812%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5b812333-dca2-d3c8-b81e-8afd2e094be6; UM_distinctid=165707184f2394-0804572d9e93fb-37664109-144000-165707184f4385; __mfwlv=1535202472; __mfwvn=2; CNZZDATA30065558=cnzz_eid%3D1321917430-1535187057-null%26ntime%3D1535197857; __mfwlt=1535202516',
        'Host': 'www.mafengwo.cn',
        'Referer': 'http://www.mafengwo.cn/gonglve/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

    }
#获得目的地热门景点总评论数
def get_jd():
    global data
    global headers
    citys=[]
    numbers=[]
    for id in data['id']:
        try:
            number=0
            url='http://www.mafengwo.cn/jd/{0}/gonglve.html'.format(id)
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            city=html.xpath('//*[@id="container"]/div[1]/div/div[1]/div[3]/div/span/a/text()')[0]
            counts=html.xpath('//*[@id="container"]/div[3]/div/div')
            for count in counts:
                number+=int(count.xpath('./div[1]/div/h3/a[2]/span/em/text()')[0])
            citys.append(city)
            numbers.append(number)
        except:
            continue
    jd=pd.DataFrame({'city':citys,'number':numbers})
    jd.to_excel('热门景点.xlsx')

#获得热门目的地游记数量
def get_yj():
    global data
    global headers
    browser = webdriver.Chrome()
    citys=[]
    totals=[]
    for id in data['id']:
        try:
            url = 'http://www.mafengwo.cn/yj/{0}/2-0-1.html'.format(id)
            browser.get(url)
            response =browser.page_source
            html = etree.HTML(response)
            city=html.xpath('/html/body/div[2]/div[1]/div[3]/div/span/a/text()')[0]
            total=html.xpath('/html/body/div[2]/div[4]/div/div[4]/div/span[1]/span[2]/text()')[0]
            citys.append(city)
            totals.append(total)
        except:
            continue
    youji=pd.DataFrame({'city':citys,'total':totals})
    youji.to_excel('游记表.xlsx')
    browser.close()

#获得热门目的地印象标签
def get_xc():
    global data
    foods = []
    sights = []
    happys = []
    citys=[]
    browser = webdriver.Chrome()
    for id in data['id']:
        try:
            url = 'http://www.mafengwo.cn/xc/{0}/'.format(id)
            food=0
            sight=0
            happy=0
            browser.get(url)
            response=browser.page_source
            html = etree.HTML(response)
            city=html.xpath('/html/body/div[2]/div[1]/div[3]/div/span/a/text()')[0]
            tags=html.xpath('/html/body/div[2]/div[5]/div[1]/div[2]/ul/li')
            for tag in tags:
                tag_=re.findall('\w+',tag.xpath('./a/@href')[0])[0]
                tag_number=tag.xpath('./a/em/text()')[0]
                if tag_ == 'cy':
                    food+=int(tag_number)
                elif tag_=='jd':
                    sight+=int(tag_number)
                else:
                    happy+=int(tag_number)
            foods.append(food)
            sights.append(sight)
            happys.append(happy)
            citys.append(city)
        except:
            continue
    xingcheng=pd.DataFrame({'city':citys,'food':foods,'sight':sights,
                            'happy':happys})
    xingcheng.to_excel('标签表.xlsx')
    browser.close()

#获得目的地TOP5各个景点评论数
def getjdinfo():
    global data
    global headers
    jds = []
    numbers = []
    for id in data['id']:
        try:
            url = 'http://www.mafengwo.cn/jd/{0}/gonglve.html'.format(id)
            response = requests.get(url, headers=headers).text
            html = etree.HTML(response)
            city = html.xpath('//*[@id="container"]/div[1]/div/div[1]/div[3]/div/span/a/text()')[0]
            counts = html.xpath('//*[@id="container"]/div[3]/div/div')
            for count in counts:
                number= int(count.xpath('./div[1]/div/h3/a[2]/span/em/text()')[0])
                jd=city+'·'+count.xpath('./div[1]/div/h3/a[1]/text()')[0]
                print(jd,number)
                jds.append(jd)
                numbers.append(number)
        except:
            continue
    jd = pd.DataFrame({'sight': jds, 'number': numbers})
    jd.to_excel('景点人气.xlsx')


#获得美食信息
def get_food():
    global data
    global headers
    foods_=[]
    foods_number=[]
    for id in data['id']:
        try:
            url = 'http://www.mafengwo.cn/cy/{0}/gonglve.html'.format(id)
            response = requests.get(url, headers=headers).text
            html = etree.HTML(response)
            foods = html.xpath('/html/body/div[3]/div[1]/div[2]/div/ol/li')
            city=html.xpath('/html/body/div[2]/div[1]/div[3]/div/span/a/text()')[0]
            for food in foods:
                food_=city+'·'+food.xpath('./a/h3/text()')[0]
                food_number=food.xpath('./a/span[2]/text()')[0]
                foods_.append(food_)
                foods_number.append(food_number)
        except:
            continue
    foo = pd.DataFrame({'name': foods_, 'city':foods_number})
    foo.to_excel('美食排名.xlsx')



if __name__ == '__main__':
    get_xc()
    get_yj()
    get_jd()
    getjdinfo()
    get_food()
