from selenium import webdriver
from lxml import etree
from pyecharts import Map,Bar, Line, Overlap,Page

#获取卫视实时收视率
browser=webdriver.Chrome()
url='http://www.csm-huan.com/index_weishi.html'
rates=[]
city=[]
browser.get(url)
html=etree.HTML(browser.page_source)
results=html.xpath('//*[@id="tbody"]/tr')
for result in results:
    media=result.xpath('./td[1]/a/text()')[0].replace('卫视', '')
    if media!='兵团' and media != '旅游':
        if media=='东方':
            media='上海'
        if media=='东南':
            media = '福建'
        city.append(media),
        rates.append(result.xpath('./td[3]/a/span')[0].text.replace('%',''))
    else:
        continue
'''
卫视时段数据爬虫
results=html.xpath('//*[@id="mCSB_1_container"]/table/tbody/tr')

for result in results:
    media=re.findall('[\u4e00-\u9fa5]+', result.xpath('./td[1]/a')[0].text)[0].replace('卫视', '')

    if media!='兵团' and media != '旅游':
        if media=='东方':
            media='上海'
        if media=='东南':
            media = '福建'
        city.append(media),
        rates.append(result.xpath('./td[2]/a')[0].text.replace('%',''))
    else:
        continue
'''

print(city)
print(rates)
'''
map = Map("全国卫视频道2018/08/13 (18:00-24:00)实时收视率", width=1200, height=600)
map.add(
    "",
    city,
    rates,
    maptype="china",
    is_visualmap=True,
    visual_text_color="#000",
    visual_range=[0, 1]
)
map.render()
map


from pyecharts import Map,Bar, Line, Overlap

8.13 18:00-24:00
city=['湖南', '江苏', '山东', '浙江', '江西', '北京', '上海', '黑龙江', '安徽', '重庆', '福建', '辽宁', '贵州', '深圳', '湖北', '广西', '广东', '河北', '天津', '四川', '山西', '河南', '内蒙古', '吉林', '陕西', '云南', '宁夏', '青海', '新疆', '甘肃', '西藏']
rates=['0.8177', '0.3846', '0.3529', '0.2839', '0.2044', '0.1953', '0.1816', '0.1386', '0.1339', '0.1229', '0.0979', '0.0975', '0.0788', '0.0765', '0.0730', '0.0657', '0.0631', '0.0604', '0.0594', '0.0548', '0.0510', '0.0477', '0.0437', '0.0435', '0.0407', '0.0308', '0.0254', '0.0253', '0.0208', '0.0190', '0.0097']

map = Map("全国卫视频道2018/08/13 (18:00-24:00)实时收视率", width=1200, height=800)
map.add(
    "",
    city,
    rates,
    maptype="china",
    is_visualmap=True,
    visual_text_color="#000",
    visual_range=[0, 1]
)
map.render()
bar = Bar("实时收视率折线图",title_pos="left",width=1800, height=1000)
bar.add("城市", city, rates,xaxis_rotate=70)
line = Line(width=1800, height=1000)
line.add("收视率", city, rates, mark_point=["max","min"],xaxis_rotate=30)
overlap = Overlap()
overlap.add(bar)
overlap.add(line)
overlap.render()
overlap
'''