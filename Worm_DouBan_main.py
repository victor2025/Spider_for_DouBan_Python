# coding=utf-8

import sys
from bs4 import BeautifulSoup as bs     #网页解析，获取数据
import re               #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url,获取网络数据
import xlwt             #进行excel操作
import sqlite3          #进行SQLite数据库操作
from re_Setting import ReSetting
import get_functions


def main():
    save_path = r".\Data_result\Douban_TOP_250.xls"
    base_url="https://movie.douban.com/top250"
    re_setting = ReSetting()
    #1.爬取网页
    data_list = getData(base_url,re_setting)

    #3.保存数据
    # saveData(save_path)

#爬取网页,逐一解析数据
def getData(base_url,re_setting):
    data_list = []
    for i in range(0,1):   #调用获取页面信息的函数，10次
        url = base_url + "?start=" + str(i*25)
        html=askURL(url)    #保存获取到的网页资源
        #逐一解析数据
        soup = bs(html,"html.parser")
        for item in soup.find_all("div",class_="item"):
            # print(item) #测试，用来查看电影item所有信息
            # data = []   #保存一部电影的所有信息
            item = str(item)
            data = get_functions.get_all(re_setting,item)
            data_list.append(data)

    print(data_list)
    return data_list

# 得到指定url中的内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }   #用户代理表示告诉服务器，我们是什么类型的设备/浏览器
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#保存数据
def saveData(save_path):
    return 0


if __name__ == "__main__":      #当程序执行时
    # 调用函数
    main()