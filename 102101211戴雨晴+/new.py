from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
import re
import time
import requests
import csv

real_list = []
f=open('data.csv',mode='w' , newline='', encoding='utf-8')
csv_write= csv.DictWriter(f, fieldnames=['弹幕时间','弹幕内容'])
csv_write.writeheader()

def get_bv(urls):
    # 配置Microsoft Edge浏览器的驱动路径
    driver_path = 'D:\py\python\msedgedriver.exe'
    # 创建Microsoft Edge浏览器的选项
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('--headless')  # 无头模式
    # 创建Microsoft Edge浏览器驱动
    driver = Edge(executable_path=driver_path, options=edge_options)
    for url in urls:
        # 打开网页
        driver.get(url)

        # 等待页面加载完全
        time.sleep(0.5)

        # 获取页面源代码
        html = driver.page_source

        bv = re.findall(r'(BV.{10})', html)
        # 去重
        for a in bv:
            if real_list.count(a) == 0:
                real_list.append(a)
    # 关闭浏览器驱动
    driver.quit()
    return real_list

# 爬取300个视频弹幕网址
def do_barrage(bvs):
    for i in bvs[:300]:
        # 构造弹幕请求地址
        url= f'https://api.bilibili.com/x/web-interface/view?bvid={i}'
        # 发送请求并获取视频信息
        response= requests.get(url)
        video= response.json()
        # 提取视频的弹幕 oid
        oid= video['data']['cid']
        # 构造弹幕地址
        barrage= f'https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'
        barrage_re= requests.get(barrage)
        barrage_re.encoding= 'utf-8'
        #解析数据
        ba_list =re.findall('<d p="(.*?)">(.*?)</d>',barrage_re.text)
    # 将弹幕存进文本中
        for time,content in ba_list:
            barrages={'弹幕时间': time,'弹幕内容':content}
            csv_write.writerow(barrages)
    f.close()
# 调用函数获取链接列表
urls=[]
ui="https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=5"
urls.append(ui)
for i in range(1,20):
    ui=f"https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page={i}&o={30*i}"
    urls.append(ui)
bvs = get_bv(urls)
print("爬虫视频数量",len(bvs))
do_barrage(bvs) #处理弹幕

