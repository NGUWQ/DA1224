from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import time
import pymongo
#利用selenium模拟用户操作获取去哪儿自由行数据(全国)

def get():
    url='https://fh.dujia.qunar.com/?tf=package'
    browser=webdriver.Chrome()
    wait=WebDriverWait(browser,30)
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.ID,'depCity')))
    dep=browser.find_element_by_id('depCity')
    dep.clear()
    dep.send_keys('深圳')
    arr=browser.find_element_by_id('arrCity')
    arr.send_keys('三亚')
    click=browser.find_element_by_class_name('js_submit')
    click.click()
    index = 8
    page=1
    while int(page)<3:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#list .item')))
        page = browser.find_element_by_css_selector('#pager > div > em').text
        response=browser.page_source
        doc=pq(response)
        items=doc('#list .item').items()
        for item in items:
            content={
                '标题':item.find('.e_box.cf > h4 > a').text(),
                '价格':item.find('.pack .avgPrice').text()
            }
            print(content)
            savetomongo(content)
        time.sleep(3)
        nextpage_btn=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pager > div > a:nth-child({})'.format(index))))
        index=index+1
        nextpage_btn.click()
    browser.close()


mongouri='localhost'
mongodb='qunars'
collection='travel'
client=pymongo.MongoClient(mongouri)
db=client[mongodb]

def savetomongo(content):
    db[collection].insert(content)



if __name__ == '__main__':
    get()
