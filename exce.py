import pandas as pd
from collections import Counter
import csv
import jieba
import wordcloud
import matplotlib.pyplot as plt

#文件读出
def read_csv(content_list ):
    top= Counter(content_list) #求出各弹幕的数量
    top_barrage =top.most_common(20)#得到弹幕数量前20的数据
    # 创建文件，得出弹幕数量前20的数据的csv文件
    f = open('count.csv', mode='w', newline='', encoding='utf-8')
    csv_write = csv.DictWriter(f, fieldnames=['弹幕内容', '弹幕数量'])
    csv_write.writeheader()
    top20_barrage = {}
    for contenty,count in top_barrage :
        top20_barrage= {'弹幕内容': contenty,'弹幕数量':count}
        csv_write.writerow(top20_barrage)
    f.close()

#词云图
def cyu_pic(content_list):
    content =' '.join(content_list)#分离弹幕句子
    txt =jieba.lcut(content)#将句子分散成词
    string =' '.join(txt)#使词分开
    #画词云图
    cu =wordcloud.WordCloud(
    height=700,
    width=1000,
    font_path='msyh.ttc',
    stopwords={'啊','了','吗','是','我','的','有','都','你','他','他们'} #删除无用词
    )
    cu.generate(string)
    cu.to_file('日本核污水.png')
    plt.imshow(cu)

# 读出文件中弹幕内容
data = pd.read_csv('data.csv')
content_list = [i for i in data['弹幕内容']]
read_csv(content_list ) #得出excel排名表
cyu_pic(content_list )#得出词云图