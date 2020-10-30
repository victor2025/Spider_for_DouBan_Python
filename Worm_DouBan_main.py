# coding=utf-8

import sys
from bs4 import BeautifulSoup as bs     #网页解析，获取数据
import re               #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url,获取网络数据
import xlwt             #进行excel操作
import sqlite3          #进行SQLite数据库操作


def main():
    save_path = r".\Data_result\Douban_TOP_250.xls"
    base_url="https://movie.douban.com/top250"
    #1.爬取网页
    data_list = getData(base_url)

    #3.保存数据
    # saveData(save_path)

# 影片详情链接的规则，只会查找到括号里面的内容
find_link = re.compile(r'<a href="(.*?)">')    #创建正则表达式对象，表示规则（字符串的模式）
# 影片图片链接，re.S让换行符包含在字符中
find_img_link = re.compile(r'<img.*src="(.*?)"',re.S)
# 影片片名
find_title = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
find_judge_number = re.compile(r'<span>(\d*)人评价</span>')
# 电影概况
find_inq = re.compile(r'<span class="inq">(.*)</span>')
# 相关内容
find_bd = re.compile(r'<p class="">(.*?)</p>',re.S)
# find_movie_name=re.compile(r'<img alt="(^[\u4e00-\u9fa5_a-zA-Z0-9]*)')

#爬取网页,逐一解析数据
def getData(base_url):
    data_list = []
    for i in range(0,1):   #调用获取页面信息的函数，10次
        url = base_url + "?start=" + str(i*25)
        html=askURL(url)    #保存获取到的网页资源

        #逐一解析数据
        soup = bs(html,"html.parser")
        for item in soup.find_all("div",class_="item"):
            # print(item) #测试，用来查看电影item所有信息
            data = []   #保存一部电影的所有信息
            item = str(item)
            # 获取到影片详情的链接
            link = re.findall(find_link,item)[0]     #使用re库通过正则表达式查找所有的字符串
            # print(link)
            data.append(link)   #添加链接
            img_link = re.findall(find_img_link,item)[0]

            data.append(img_link)#添加图片
            titles = re.findall(find_title,item)
            if (len(titles) == 2):
                ctitle = titles[0]  #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace('/','')#去掉无关的符号
                otitle = re.sub(r'(\xa0)*',"",otitle)
                data.append(otitle) #添加外文名
            else:
                data.append(titles)
                data.append('   ')  #外文名留空

            rating = re.findall(find_rating,item)
            data.append(rating)

            judge_number = re.findall(find_judge_number,item)
            data.append(judge_number)#添加评价人数

            inq = re.findall(find_inq,item)
            if (len(inq)!=0):
                inq = inq[0].replace('。','')    #替换掉句号
                data.append(inq)        #添加概述
            else:
                data.append('  ')   #留空

            bd = re.findall(find_bd,item)[0]
            bd = re.sub(r'<br(\s+)?/>(\s+)?',"",bd)     #去掉<br/>
            bd = re.sub(r'(\xa0)*',"",bd)
            bd = re.sub('/','',bd)
            data.append(bd.strip())

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