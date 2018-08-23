## 调用要使用的包
import json
import random
import requests
import time
import pandas as pd
import os
from pyecharts import Bar, Geo, Line, Overlap
import jieba
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter

os.chdir('C:/爬虫/一出好戏')

## 设置headers和cookie
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
          'Connection': 'keep-alive',
          'Cookie': '_lxsdk_cuid=164a8822932c8-0d8cb3970718bb-5e442e19-144000-164a8822934c8; _lxsdk=6F7FC87089C811E8A98F1964825FAF5AA4DC90F9A1A2460FBA3E881749F8BD53; v=3; __mta=212578603.1531835460263.1533864432030.1533864434849.36; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1652e65d195-6b7-e83-346%7C%7C6',
          'Host': 'm.maoyan.com'
          }

def getinfo():
    haoxi = pd.DataFrame(columns=['date', 'score', 'city', 'comment', 'nick'])
    for i in range(0,1000):
        j=random.randint(1,1000)
        print(str(i)+' '+str(j))
        try:
            time.sleep(2)
            url='http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset='+str(j)
            html=requests.get(url=url,headers=headers).content
            data=json.loads(html.decode('utf-8'))['cmts']
            for item in data:
                haoxi = haoxi.append({'date': item['time'].split(' ')[0], 'city': item['cityName'], 'score': item['score'],
                            'comment': item['content'], 'nick': item['nick']}, ignore_index=True)
            haoxi.to_excel('一出好戏3.xlsx', index=False)
        except:
            continue


#去重
def quchong():
    data = pd.read_excel('C:\爬虫\一出好戏\一出好戏new1.xlsx')
    data = data.drop_duplicates()
    data = pd.DataFrame(data)
    data.to_excel('C:\爬虫\一出好戏\一出好戏new.xlsx')


#数据分析图表
def charts():
    # 读取我们已经爬取到的数据进行分析
    haoxi_com = pd.read_excel('C:\爬虫\一出好戏\一出好戏new.xlsx')
    grouped = haoxi_com.groupby(['city'])
    grouped_pct = grouped['score']

    # 全国热力图
    city_com = grouped_pct.agg(['mean', 'count'])
    city_com.reset_index(inplace=True)
    city_com['mean'] = round(city_com['mean'], 2)
    data = [(city_com['city'][i], city_com['count'][i]) for i in range(0, city_com.shape[0])]
    geo = geo = Geo('《一出好戏》全国热力图', title_color="#fff",
                    title_pos="center", width=1200, height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, type="heatmap", visual_range=[0, 200],
            visual_text_color="#fff", symbol_size=10, is_visualmap=True,
            is_roam=False)
    geo.render('一出好戏全国热力图.html')

    # 主要城市评论数与评分
    city_main = city_com.sort_values('count', ascending=False)[0:20]
    attr = city_main['city']
    v1 = city_main['count']
    v2 = city_main['mean']
    line = Line("《一出好戏》主要城市评分")
    line.add("分数", attr, v2, is_stack=True, xaxis_rotate=30,
             mark_point=['min', 'max'], xaxis_interval=0, line_color='lightblue',
             line_width=4, mark_point_textcolor='black', mark_point_color='lightblue',
             is_splitline_show=False)

    bar = Bar("《一出好戏》主要城市评论数")
    bar.add("城市", attr, v1, is_stack=False, xaxis_rotate=30,
            xaxis_interval=0, is_splitline_show=False)
    overlap = Overlap()
    # 默认不新增 x y 轴，并且 x y 轴的索引都为 0
    overlap.add(bar)
    overlap.add(line, yaxis_index=1, is_add_yaxis=True)
    overlap.render('一出好戏主要城市评论数_平均分.html')

    # 主要城市评分降序
    city_score = city_main.sort_values('mean', ascending=False)
    attr = city_score['city']
    v1 = city_score['mean']
    line = Line("《一出好戏》主要城市评分")
    line.add("城市", attr, v1, is_stack=True, xaxis_rotate=30,
             mark_point=['min', 'max'], xaxis_interval=0, line_color='lightblue',
             line_width=4, mark_point_textcolor='black', mark_point_color='lightblue',
             is_splitline_show=False)
    line.render('一出好戏主要城市评分.html')

    # 主要城市评分全国分布
    city_score_area = city_com.sort_values('count', ascending=False)[0:30]
    city_score_area.reset_index(inplace=True)
    data = [(city_score_area['city'][i], city_score_area['mean'][i]) for i in range(0,
                                                                                    city_score_area.shape[0])]
    geo = Geo('《一出好戏》全国主要城市打分图', title_color="#fff",
              title_pos="center", width=1200, height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value,
            visual_text_color="#fff", symbol_size=15, is_visualmap=True,
            is_roam=False, visual_range=[0, 200])
    geo.render('一出好戏全国主要城市打分图.html')

    # 绘制词云
    haoxi_str = ' '.join(haoxi_com['comment'])
    words_list = []
    word_generator = jieba.cut_for_search(haoxi_str)
    for word in word_generator:
        words_list.append(word)
    words_list = [k for k in words_list if len(k) > 1]
    back_color = imread('C:/爬虫/一出好戏/haoxi.jpg')  # 解析该图片
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=200,  # 最大词数
                   mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=300,  # 显示字体的最大值
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   )
    haoxi_count = Counter(words_list)
    wc.generate_from_frequencies(haoxi_count)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(back_color)
    # 绘制结果
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    plt.savefig('2.png', dpi=400)
    plt.show()








if __name__ == '__main__':
    #getinfo()
    quchong()