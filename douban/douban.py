from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
import re
import pandas as pd

browser=webdriver.Chrome()
def getId():
    url='https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%B0%E6%B9%BE'
    tv = pd.DataFrame(columns=['id', 'name'])
    browser.get(url)
    wait=WebDriverWait(browser,10)
    for i in range(40):
        js="var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(3)
        next=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div > div.article > a')))
        next.click()
        print(i)
    time.sleep(3)
    html=browser.page_source
    html=etree.HTML(html)
    items=html.xpath('//*[@id="app"]/div/div[1]/div[@class="list-wp"]/a')
    for item in items:
        name=item.xpath('./p/span[1]')[0].text
        id=re.findall('\d+',item.xpath('./@href')[0])[0]
        tv=tv.append({'id':id,'name':name},ignore_index=True)
    tv.to_excel('电视剧id表.xlsx')



def getinfo():

    data=pd.read_excel('C:/daima/dataanalysis/douban/id.xlsx')
    base_url='https://movie.douban.com/subject/{0}/'
    tv = pd.DataFrame(columns=['编号', '名称','年份','主演1',
                               '主演2','次主演1','次主演2','次主演3',
                               '评分','评分人数','剧情简介'])
    flag = True
    for id in data['id']:
        try:
            time.sleep(3)
            url=base_url.format(id)
            browser.get(url)
            response = browser.page_source
            html = etree.HTML(response)
            '''
            if flag:
                login = browser.find_element_by_css_selector('body > a')
                login.click()
                email = browser.find_element_by_id('email')
                email.clear()
                email.send_keys('1373734675@qq.com')
                password = browser.find_element_by_id('password')
                password.send_keys('wq1996122421')
                btn = browser.find_element_by_class_name('btn-submit')
                btn.click()
                time.sleep(1)
                response = browser.page_source
                html = etree.HTML(response)
                flag=False
            '''
            name = html.xpath('//*[@id="content"]/h1/span[1]')[0].text
            year = re.findall('\d+', html.xpath('//*[@id="content"]/h1/span[2]')[0].text)[0]
            actor1 = html.xpath('//*[@id="info"]/span[3]/span[2]/span[1]/a/text()')[0]
            actor2 = html.xpath('//*[@id="info"]/span[3]/span[2]/span[2]/a/text()')[0]
            actor3 = html.xpath('//*[@id="info"]/span[3]/span[2]/span[3]/a/text()')[0]
            actor4 = html.xpath('//*[@id="info"]/span[3]/span[2]/span[4]/a/text()')[0]
            actor5 = html.xpath('//*[@id="info"]/span[3]/span[2]/span[5]/a/text()')[0]
            score = html.xpath('//*[@id="interest_sectl"]/div/div[2]/strong')[0].text
            people = html.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span')[0].text
            intro = re.findall('[^\x00-\xff]+', html.xpath('//*[@id="link-report"]/span[1]/span/text()')[0])[0]
            tv=tv.append({'编号':id,'名称':name,'年份':year,'主演1':actor1,
                          '主演2':actor2,'次主演1':actor3,'次主演2':actor4,
                          '次主演3':actor5,'评分':score,'评分人数':people,'剧情简介':intro},ignore_index=True)
            tv.to_excel('douban2.xlsx')
            print('1')

        except:
            continue



if __name__ == '__main__':
    getinfo()