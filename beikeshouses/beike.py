import requests
import pandas as pd
from lxml import etree
import os
import time


os.chdir('C:/爬虫/深圳租房')

headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'cookie':'lianjia_uuid=6a94fff5-1c8f-4db3-af7f-894e4583e2ad; _smt_uid=5b7e359e.24c42723; ke_uuid=cbe1f4b1e4c50ee6aea047d6318a52c2; _ga=GA1.2.1818174679.1534998047; UM_distinctid=1656f15d8f83d-0596b4bb0bc6a9-37664109-144000-1656f15d8fab02; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22165650174701f3-05b29e21be9cd8-37664109-1327104-165650174725fa%22%2C%22%24device_id%22%3A%22165650174701f3-05b29e21be9cd8-37664109-1327104-165650174725fa%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fs%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22sousuo%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; www_zufangzi_server=0ca0f641b9b44a3586617f59ad4d8f06; lianjia_ssid=d79dd134-7891-4896-aa6c-25a5fdb75a9c; CNZZDATA1273627291=250116370-1535536415-https%253A%252F%252Fsz.ke.com%252F%7C1535626418',
'Host': 'sz.zu.ke.com',
'Referer': 'https://sz.zu.ke.com/zufang/rt200600000001/',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

}



def gethousehezu(area):
    """
    获取贝壳深圳合租房url
    :param area:
    :return:
    """
    areas=getareas(area)
    houses = pd.DataFrame(columns=['链接'])
    base_url = 'https://sz.zu.ke.com/zufang/{0}/pg'.format(area)
    for page in range(1,27):
        try:
            time.sleep(1)
            url=base_url+str(page)+'rt200600000002/#contentList'
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items = html.xpath('//*[@id="content"]/div[1]/div[1]/div')
            for item in items:
                href = item.xpath('./a/@href')[0]
                houses=houses.append({'链接':href,'地区':areas},ignore_index=True)
            houses.to_excel('合租房url表.xlsx')
            print(url)
        except:
            continue

def gethousezhengzu(area):
    """
        获取贝壳深圳整租房url
        :param area:
        :return:
        """
    areas = getareas(area)
    houses2 = pd.DataFrame(columns=['链接'])
    base_url = 'https://sz.zu.ke.com/zufang/{0}/pg'.format(area)
    for page in range(1, 73):
        try:
            time.sleep(1)
            url=base_url+str(page)+'rt200600000001/#contentList'
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items = html.xpath('//*[@id="content"]/div[1]/div[1]/div')
            for item in items:
                href = item.xpath('./a/@href')[0]
                houses2=houses2.append({'链接':href,'地区':areas},ignore_index=True)
            houses2.to_excel('整租房url表2.xlsx')
            print(url)
        except:
            continue

def gethousehezuinfo():
    """
    获取深圳合租房源信息
    :return:
    """
    data=pd.read_excel('C:/爬虫/深圳租房/合租房url表.xlsx')
    base_url='https://sz.zu.ke.com{0}?nav=200600000002'
    house=pd.DataFrame(columns=['房源','价格','面积','地区'])
    for i in range(len(data['链接'])):
        try:
            time.sleep(0.5)
            url=base_url.format(data['链接'][i])
            response = requests.get(url, headers=headers).text
            html = etree.HTML(response)
            name = html.xpath('/html/body/div[3]/div[1]/div[3]/p/text()')[0]
            price = html.xpath('//*[@id="aside"]/p[1]/span/text()')[0]
            square = html.xpath('//*[@id="aside"]/ul[1]/p/span[3]/text()')[0]
            house=house.append({'房源':name,'价格':price,'面积':square,'地区':data['地区'][i]},ignore_index=True)
            house.to_excel('深圳合租房信息.xlsx')
            print('已完成'+str(i))

        except:
            continue


def gethousezhengzuinfo():
    """
    获取深圳整租房源信息
    :return:
    """
    data = pd.read_excel('C:/爬虫/深圳租房/整租房url表.xlsx')
    base_url = 'https://sz.zu.ke.com{0}?nav=200600000001'
    house = pd.DataFrame(columns=['房源', '价格', '面积', '地区','朝向','租房类型','大小'])
    for i in range(len(data['链接'])):
        try:
            url = base_url.format(data['链接'][i])
            response = requests.get(url, headers=headers).text
            html = etree.HTML(response)
            name = html.xpath('/html/body/div[3]/div[1]/div[3]/p/text()')[0]
            price = html.xpath('//*[@id="aside"]/p[1]/span/text()')[0]
            square = html.xpath('//*[@id="aside"]/ul[1]/p/span[3]/text()')[0]
            large = html.xpath('//*[@id="aside"]/ul[1]/p/span[2]/text()')[0]
            direction = html.xpath('//*[@id="aside"]/ul[1]/p/span[4]/text()')[0]
            house = house.append({'房源': name, '价格': price, '面积': square, '地区': data['地区'][i],
                                  '朝向':direction,'租房类型':'整租','大小':large}, ignore_index=True)
            house.to_excel('深圳整租房信息.xlsx')
            print('已完成' + str(i))

        except:
            continue


def gethousezhengzuinfo2():
    """
    获取深圳整租房源公寓信息
    :return:
    """
    data = pd.read_excel('C:/爬虫/深圳租房/整租房url表2.xlsx')
    base_url = 'https://sz.zu.ke.com{0}?nav=200600000001'
    house = pd.DataFrame(columns=['房源', '价格','租房类型'])
    for i in range(len(data['链接'])):
        try:
            url = base_url.format(data['链接'][i])
            response = requests.get(url, headers=headers).text
            html = etree.HTML(response)
            name = html.xpath('//*[@id="aside"]/p/span[1]/text()')[0].strip()
            price = html.xpath('//*[@id="aside"]/p/span[2]/text()')[0].strip()
            house = house.append({'房源': name, '价格': price, '租房类型': '整租','地区':data['地区'][i]}, ignore_index=True)
            house.to_excel('深圳整租房信息3.xlsx')
            print('已完成' + str(i))

        except:
            continue




def getareas(area):
    if area=='luohuqu':
        areas='罗湖区'
    elif area=='futianqu':
        areas = '福田区'
    elif area=='nanshanqu':
        areas = '南山区'
    elif area=='baoanqu':
        areas = '宝安区'
    elif area=='longgangqu':
        areas = '龙岗区'
    elif area=='longhuaqu':
        areas = '龙华区'
    elif area=='yantianqu':
        areas = '盐田区'
    elif area=='guangmingxinqu':
        areas = '光明新区'
    elif area=='pingshanqu':
        areas = '坪山区'
    elif area=='dapengxinqu':
        areas = '大鹏新区'
    return areas


if __name__ == '__main__':
    '''
    #areas=['luohuqu','futianqu','nanshanqu','baoanqu','longgangqu','longhuaqu']
    areas = ['yantianqu','guangmingxinqu','pingshanqu','dapengxinqu']
    for area in areas:
        gethousezhengzu(area)
    '''
    #gethousehezuinfo()
    #gethousezhengzuinfo()
    gethousezhengzuinfo2()