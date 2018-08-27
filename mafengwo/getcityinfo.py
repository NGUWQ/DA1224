import os
import re
import requests
from lxml import etree
import pandas as pd

os.chdir('C:/爬虫/蚂蜂窝')


#获得地区id列表
def get_area_url(url):
    city_name=[]
    city_id=[]
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
    response=requests.get(url,headers=headers).text
    html=etree.HTML(response)
    items=html.xpath('//div[2]/div[2]/div/div[3]/div[1]/div/dl')
    for item in items:
        try:
            id=[re.findall('\d+',i)[0]for i in item.xpath('./dd/a/@href')]
            city=item.xpath('./dd/a/text()')
            #print(id,city)
            city_id.extend(id)
            city_name.extend(city)
        except:
            continue
    return city_id,city_name



if __name__ == '__main__':
    url='http://www.mafengwo.cn/mdd/'
    id,name=get_area_url(url)
    city=pd.DataFrame({'id':id,'city':name})
    city.to_excel('国内热门目的地.xlsx')