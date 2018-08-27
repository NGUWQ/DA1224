import pandas as pd
data=pd.read_excel('C:/爬虫/蚂蜂窝/国内热门目的地.xlsx')
for id in data['id']:
    print(id)