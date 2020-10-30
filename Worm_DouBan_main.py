# coding=utf-8

import sys
from bs4 import BeautifulSoup as bs     #网页解析，获取数据
import re               #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url,获取网络数据
import xlwt             #进行excel操作
import sqlite3          #进行SQLite数据库操作
from re_Setting import ReSetting
import get_functions
import major_functions


def main():
    save_path = r"Douban_TOP_250.xls"
    base_url="https://movie.douban.com/top250"
    re_setting = ReSetting()
    #1.爬取网页
    data_list = getData(base_url,re_setting)

    #3.保存数据
    saveData(save_path,data_list)

#爬取网页,逐一解析数据
def getData(base_url,re_setting):
    data_list = major_functions.major_data_get(base_url,re_setting) # 获取网页数据
    print(data_list)
    return data_list

#保存数据
def saveData(save_path,data_list):
    work_book = xlwt.Workbook(encoding="utf-8")
    work_sheet = work_book.add_sheet("豆瓣电影top250")
    for i in range(0,len(data_list)):
        for j in range(0,len(data_list[0])):
            work_sheet.write(i,j,data_list[i][j])
    work_book.save(save_path)

if __name__ == "__main__":      #当程序执行时
    # 调用函数
    main()