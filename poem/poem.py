import requests
from lxml import etree
from selenium import webdriver
import pandas as pd
import os
import time

headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cookie': 'ASP.NET_SessionId=lepd22lrt5uqioo5s25j5p23; Hm_lvt_04660099568f561a75456483228a9516=1534664307; Hm_lpvt_04660099568f561a75456483228a9516=1534669012',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}



def poetry():
    baseurl='https://www.gushiwen.org/shiwen/default_4A1A{0}.aspx'
    poems = pd.DataFrame(columns=['title', 'dynasty', 'name', 'good'])
    for page in range(1,1000):
        try:
            url=baseurl.format(str(page))
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items=html.xpath('//div[2]/div[1]/div[@class="sons"]')
            for item in items:
                try:
                    title=item.xpath('./div[1]/p[1]/a/b')[0].text
                    dynasty=item.xpath('./div[1]/p[2]/a[1]')[0].text
                    name=item.xpath('./div[1]/p[2]/a[2]')[0].text
                    good=item.xpath('./div[@class="tool"]/div[@class="good"]/a/span')[0].text
                    poems=poems.append({'title':title,'dynasty':dynasty,'name':name,'good':good},ignore_index=True)

                except:
                    continue
            poems.to_excel('诗.xlsx')
            print(page)
            time.sleep(2)
        except:
            continue

def words():
    baseurl='https://www.gushiwen.org/shiwen/default_4A2A{0}.aspx'
    poems = pd.DataFrame(columns=['title', 'dynasty', 'name', 'good'])
    for page in range(1,1000):
        try:
            url=baseurl.format(str(page))
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items=html.xpath('//div[2]/div[1]/div[@class="sons"]')
            for item in items:
                try:
                    title=item.xpath('./div[1]/p[1]/a/b')[0].text
                    dynasty=item.xpath('./div[1]/p[2]/a[1]')[0].text
                    name=item.xpath('./div[1]/p[2]/a[2]')[0].text
                    good=item.xpath('./div[@class="tool"]/div[@class="good"]/a/span')[0].text
                    poems=poems.append({'title':title,'dynasty':dynasty,'name':name,'good':good},ignore_index=True)

                except:
                    continue
            poems.to_excel('词.xlsx')
            print(page)
        except:
            continue

def bends():
    baseurl='https://www.gushiwen.org/shiwen/default_4A3A{0}.aspx'
    poems = pd.DataFrame(columns=['title', 'dynasty', 'name', 'good'])
    for page in range(1,146):
        try:
            url=baseurl.format(str(page))
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items=html.xpath('//div[2]/div[1]/div[@class="sons"]')
            for item in items:
                try:
                    title=item.xpath('./div[1]/p[1]/a/b')[0].text
                    dynasty=item.xpath('./div[1]/p[2]/a[1]')[0].text
                    name=item.xpath('./div[1]/p[2]/a[2]')[0].text
                    good=item.xpath('./div[@class="tool"]/div[@class="good"]/a/span')[0].text
                    poems=poems.append({'title':title,'dynasty':dynasty,'name':name,'good':good},ignore_index=True)

                except:
                    continue
            poems.to_excel('曲.xlsx')
            print(page)
            time.sleep(1)
        except:
            continue


def ancient():
    baseurl='https://www.gushiwen.org/shiwen/default_4A4A{0}.aspx'
    poems = pd.DataFrame(columns=['title', 'dynasty', 'name', 'good'])
    for page in range(1,61):
        try:
            url=baseurl.format(str(page))
            response=requests.get(url,headers=headers).text
            html=etree.HTML(response)
            items=html.xpath('//div[2]/div[1]/div[@class="sons"]')
            for item in items:
                try:
                    title=item.xpath('./div[1]/p[1]/a/b')[0].text
                    dynasty=item.xpath('./div[1]/p[2]/a[1]')[0].text
                    name=item.xpath('./div[1]/p[2]/a[2]')[0].text
                    good=item.xpath('./div[@class="tool"]/div[@class="good"]/a/span')[0].text
                    poems=poems.append({'title':title,'dynasty':dynasty,'name':name,'good':good},ignore_index=True)

                except:
                    continue
            poems.to_excel('文.xlsx')
            print(page)
        except:
            continue


def concat():
    """
    诗词曲文合并
    :return:
    """
    ds=pd.read_excel('C:/daima/dataanalysis/poem/诗.xlsx')
    dc=pd.read_excel('C:/daima/dataanalysis/poem/词.xlsx')
    pd.concat([ds,dc])



def infobaidu():
    """
    获取诗人百度热度
    :return:
    """
    browser=webdriver.Chrome()
    poems = pd.DataFrame(columns=['name', 'hot', 'enjoy'])
    data=pd.read_excel('C:/daima/dataanalysis/poem/100.xlsx')
    base_url='https://baike.baidu.com/item/{0}'
    for name in data['name']:
        try:
            url=base_url.format(name)
            browser.get(url)
            time.sleep(1)
            response = browser.page_source
            html = etree.HTML(response)
            hot = html.xpath('//*[@id="j-top-vote"]/span[@class="vote-count"]')[0].text
            enjoy = html.xpath('//*[@id="j-topShareCount"]')[0].text
            poems=poems.append({'name':name,'hot':hot,'enjoy':enjoy},ignore_index=True)
            poems.to_excel('102.xlsx')
            time.sleep(1)

        except:
            continue



if __name__ == '__main__':
    #ancient()
    #concat()
    infobaidu()