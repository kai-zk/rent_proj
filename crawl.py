import time
from bs4 import BeautifulSoup
import requests
import csv

url = "http://sh.58.com/pinpaigongyu/pn/{page}/?minprice=600_1000"

# 已完成的页面序号，初始为1
page = 1

csv_file = open('rent.csv','w')
# 打开writer对象，指定文件与分隔符
csv_writer = csv.writer(csv_file,delimiter=',')

while True:
    time.sleep(1)
    page +=1
    print('fetch:',url.format(page=page))
    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Referer": url.format(page=page)
    }
    response = requests.get(url.format(page=page),headers=header)
    # 创建一个BeautifulSoup对象
    html = BeautifulSoup(response.text)
    # 获取class=list的元素下的所有li元素
    house_list = html.select(".list > li")

    # 循环在读不到新的房源时结束
    if not house_list:
        break

    for house in house_list:
        # 得到标签包裹着的文本
        house_title = house.select('h2')[0].string
        house_url = "http://sh.58.com/%s" % (house.select("a")[0]['href'])
        house_info_list = house_title.split()
        house_location = house_info_list[1]

        house_money = house.select(".money")[0].select('b')[0].string
        # 写一行数据
        csv_writer.writerow([house_title,house_location,house_money,house_url])
# 关闭文件
csv_file.close()
