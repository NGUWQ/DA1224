from lxml import etree
from selenium import webdriver
import pandas as pd
import time
import csv

browser = webdriver.Chrome()
browser.get('https://www.lagou.com/jobs/list_PYTHON?px=default&city=%E5%85%A8%E5%9B%BD#filterBox')
browser.implicitly_wait(10)
data=pd.DataFrame(columns=['Name', 'Company', 'Salary', 'Education', 'Size','Welfare'])
def get_dates(selector):
        items = selector.xpath('//*[@id="s_position_list"]/ul/li')
        for item in items:
            yield {
                'Name': item.xpath('div[1]/div[1]/div[1]/a/h3/text()')[0],
                'Company': item.xpath('div[1]/div[2]/div[1]/a/text()')[0],
                'Salary': item.xpath('div[1]/div[1]/div[2]/div/span/text()')[0],
                'Education': item.xpath('div[1]/div[1]/div[2]/div//text()')[3].strip(),
                'Size': item.xpath('div[1]/div[2]/div[2]/text()')[0].strip(),
                'Welfare': item.xpath('div[2]/div[2]/text()')[0]
            }
def main():
    global data
    i = 0
    for i in range(2):
        selector = etree.HTML(browser.page_source)
        browser.find_element_by_xpath('//*[@id="order"]/li/div[4]/div[2]').click()
        time.sleep(5)
        print('第{}页抓取完毕'.format(i+1))
        for item in get_dates(selector):
            data=data.append(item,ignore_index=True)
        '''
        CSV存储
        with open('Py.csv', 'a', newline='') as csvfile:  ##Py.csv是文件的保存路径，这里默认保存在工作目录
            fieldnames = ['Name', 'Company', 'Salary', 'Education', 'Size', 'Welfare']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in get_dates(selector):
                writer.writerow(item)
        '''
        data.to_excel('Python岗位.xlsx', index=False)
        time.sleep(5)

    browser.close()
if __name__=='__main__':
    main()