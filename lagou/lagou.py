import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
import re
import pandas as pd
import time
import os

os.chdir('C:/爬虫/拉勾网')

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)
data=pd.DataFrame(columns=['Name', 'Company', 'Salary', 'Education', 'Size','Welfare'])
def getId():
    base_url='https://www.lagou.com/jobs/list_数据分析师?px=default&city=深圳&district={0}#filterBox'
    areas=['南山区','福田区','宝安区','龙岗区','龙华新区','罗湖区','盐田区','光明新区','坪山新区','大鹏新区']
    ids=[]
    areass=[]
    for area in areas:
        try:
            time.sleep(2)
            url=base_url.format(area)
            browser.get(url)
            html = browser.page_source
            html = etree.HTML(html)
            pages=html.xpath('//*[@id="order"]/li/div[4]/div[3]/span[2]/text()')[0]
            for i in range(int(pages)):
                    html = browser.page_source
                    html = etree.HTML(html)
                    items = html.xpath('//*[@id="s_position_list"]/ul/li')
                    for item in items:
                        id=re.findall('\d+',item.xpath('./div[1]/div[1]/div[1]/a/@href')[0])[0]
                        ids.append(id)
                        areass.append(area)
                        print(id+','+area+' success')
                    next=browser.find_element_by_class_name('pager_next ')
                    next.click()
                    time.sleep(1)
        except:
            continue

    positions=pd.DataFrame({
        'id':ids,'area':areass
    })
    positions.to_excel('岗位id表.xlsx')
    browser.close()

#获取职位信息
def getPosition():
    global data
    base_url = 'https://www.lagou.com/jobs/list_C?px=default&city=深圳&district={0}#filterBox'
    areas = ['南山区', '福田区', '宝安区', '龙岗区', '龙华新区', '罗湖区', '盐田区', '光明新区', '坪山新区', '大鹏新区']
    for area in areas:
        try:
            time.sleep(2)
            url = base_url.format(area)
            browser.get(url)
            html = browser.page_source
            html = etree.HTML(html)
            pages = html.xpath('//*[@id="order"]/li/div[4]/div[3]/span[2]/text()')[0]
            for i in range(int(pages)):
                time.sleep(3)
                html = browser.page_source
                html = etree.HTML(html)
                items = html.xpath('//*[@id="s_position_list"]/ul/li')
                for item in items:
                    position={
                        'Name': item.xpath('div[1]/div[1]/div[1]/a/h3/text()')[0],
                        'Company': item.xpath('div[1]/div[2]/div[1]/a/text()')[0],
                        'Salary': item.xpath('div[1]/div[1]/div[2]/div/span/text()')[0],
                        'Education': item.xpath('div[1]/div[1]/div[2]/div//text()')[3].strip(),
                        'Size': item.xpath('div[1]/div[2]/div[2]/text()')[0].strip(),
                        'Welfare': item.xpath('div[2]/div[2]/text()')[0],
                        'Area':area
                    }
                    data = data.append(position, ignore_index=True)
                    print(str(i)+','+area)
                next = browser.find_element_by_class_name('pager_next ')
                next.click()
                time.sleep(1)
            data.to_excel('C岗位.xlsx', index=False)

        except:
            continue

    browser.close()


if __name__ == '__main__':
    getPosition()