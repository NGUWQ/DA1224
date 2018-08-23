from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import csv
import pandas
import requests
import time
import random


class Travel():
    def __init__(self):
        self.browser=webdriver.Chrome()
        self.browser_ = webdriver.Chrome()
        self.wait=WebDriverWait(self.browser,10)
        self.wait_ = WebDriverWait(self.browser_, 10)
        self.csvflie = 'qunar_routes.csv'
        self.f ='haha'
        self.writer =None
        self.free='自由行'

    '''
    def init_csv(self):
        self.csvflie = 'qunar_routes.csv'
        with open(self.csvflie, 'a+', encoding='gbk') as self.f:
            self.fieldnames = ['出发地', '目的地', '路线信息', '酒店信息']
            self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
            self.writer.writeheader()
    '''

    def dump_routes_csv(self,dep,arr):
        #定位所有路线信息
        routes=self.browser.find_elements_by_css_selector('.item.g-flexbox.list-item')
        for route in routes:
            try:
                print('\nroute info:%s'%route.text)
                #获取路线详情页URL
                url=route.get_attribute('data-url')
                print('url:%s' % url)

                #在另一个浏览器对象打开路线详情页
                self.browser_.get(url)
                time.sleep(random.uniform(2,3))


                if 'fhtouch' in url:#机酒自由行
                    try:
                        self.wait_.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#allHotels')))
                        source=self.browser_.find_element_by_css_selector('#main-page')
                        target=self.browser_.find_element_by_css_selector('#allHotels')
                    except Exception as e:
                        print(str(e))
                        continue
                else:
                    try:
                        #等待页面刷新成功
                        self.wait_.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-ball.m-ball-back')))
                        source=self.browser_.find_element_by_css_selector('.flex.scrollable')
                        target=self.browser_.find_element_by_css_selector('.m-ball.m-ball-back')
                    except Exception as e:
                        print(str(e))
                        continue



                #路线详情页
                ActionChains(self.browser_).drag_and_drop(source,target).perform()

                for i in range(20):
                    # 模拟page down键的输入,实现下拉滚动条动作(5次)
                    ActionChains(self.browser_).send_keys(Keys.PAGE_DOWN).perform()

                time.sleep(3)
                '''
                #定位路线详情页下面的元素
                try:
                    #等待刷新
                    self.wait_.until(EC.presence_of_element_located(By.CSS_SELECTOR,'.tit .score'))
                except Exception as e:
                    print(str(e))
                    continue
                try:
                '''
                #获取酒店评分
                score=self.browser_.find_element_by_css_selector('.tit .score').text
                #获取酒店类型
                type=self.browser_.find_element_by_css_selector('.flex.cont > div > span').text
                #type = self.browser_.find_element_by_css_selector('.tag-list > span.g-tag.g-tag-origin.solid').text
                #拼接成酒店信息


                hotel='\n'.join([score,type])
                if hotel:
                    hotel='haha'
                print('hotel info:%s' % hotel)

                #print(score,type)

                '''
                except Exception as e:
                    print(str(e))
                    continue
                '''
                #写入csv文件
                with open('qunar_routes.csv', 'a+', newline='',encoding='gbk') as haha:
                    writers = csv.writer(haha)
                    writers.writerow([dep,arr,route.text,hotel])
                '''
                da = ['出发地', '目的地', '路线信息','酒店信息']
                content = [dep,arr,route.text,hotel]
                df = pandas.DataFrame(content,columns=da)
                df.to_csv('qunar_routes.csv', encoding='gbk')
                '''
            except:
                continue




    def main(self):
        dep_cities=['深圳']
        for dep in dep_cities:
            html=requests.get('https://touch.dujia.qunar.com/golfz/sight/arriveRecommend?dep={}&exclude=&extensionImg=255,175'.format(quote(dep)))
            arrive_cites=html.json()
            for city in arrive_cites['data']:
                if city['title']!='国内':
                    continue
                for city_1 in city['subModules']:
                    for query in city_1['items']:
                        if query['query']!='丽江':
                            continue
                        query_city=query['query']+self.free
                        #打开移动端自由行路线搜索结果页面
                        self.browser.get('https://touch.dujia.qunar.com/p/list?cfrom=zyx&dep={}&query={}&it=FreetripTouchin&et=home_free_t'.format(quote(dep),quote(query_city)))
                        '''
                        try:
                            #等待页面刷新
                            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'item g-flexbox list-item')))
                        except Exception as e:
                            print(str(e))
                            raise
                        '''
                        print('dep:%s arr:%s'%(dep,query['query']))

                        #连续下拉滚动条50次获取更多线路列表
                        for i in range(1):
                            time.sleep(random.uniform(2,3))
                            print('page %d'%(i+1))
                            #模拟page down键的输入,实现下拉滚动条动作
                            ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()

                        #将出发地到目的地的自由行路线写入CSV文件中
                        self.dump_routes_csv(dep,query['query'])


        self.browser.close()
        self.browser_.close()




if __name__ == '__main__':
    t=Travel()
    t.main()



