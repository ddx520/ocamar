# -*- coding: utf-8 -*-

# @File    : demo_01.py
# @Date    : 2021-03-21
# @Author  : ${西北彭于晏}
from bs4 import BeautifulSoup  # 网页解析
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 指定url,获取网页数据
import xlwt  # 进行excle操作
import sqlite3  # 进行sqlite数据库操作

# 创建正则表达式规则
# 影片链接规则
findLink = re.compile(r'<a href="(.*?)">')
# 图片
findImage = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中
# 影片的片名
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评价人数
findPinjia = re.compile(r'<span>(\d*)人评价</span>')
# 概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 影片相关内容*********re.S:忽视换行符
findBD = re.compile('<p class="">(.*?)</p>', re.S)


# 爬取网页
def getdata(baseurl):
    datalist = []
    for i in range(0, 10):
        # 循环10次，205条
        url = baseurl + str(i * 25)
        html = askurl(url)
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        # 查找符合要求的字符串，形成一个列表
        for item in soup.find_all('div', class_="item"):  # 查找div属性为class="item"的数据
            # print(item) #测试查看item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)  # 转型为字符串，对字符串进行re正则规则提取
            # 拿到字符串，去提取符合正则规则的数据
            title = re.findall(findTitle, item)  # 0表示只要第一个索引
            if (len(title) == 2):
                ctitle = title[0]
                data.append("中文:{0}".format(ctitle))
                otitle = title[1].replace("/", "")
                otitle = "".join(otitle.split())
                data.append("英文:{0}".format(otitle))
            else:
                data.append("片名：{0}".format(title))
                data.append(' ')
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImage, item)[0]
            data.append(imgSrc)
            Rating = re.findall(findRating, item)[0]
            data.append(Rating + "分")
            Pinjia = re.findall(findPinjia, item)[0]
            data.append(Pinjia + "人观看")
            inq = re.findall(findInq, item)[0]
            if len(inq) != 0:
                # inq=inq[0].replace("。","")  #去掉句号
                data.append(inq)
            else:
                data.append(" ")
            BD = re.findall(findBD, item)[0]
            # 替换一些换行符为空字符串
            BD = re.sub('<br(\s+)?/>(\s+)', " ", BD)
            BD = re.sub('/', " ", BD)
            BD = "".join(BD.split())
            data.append(BD.strip())  # 添加的时候去掉前后的空格
            # print(data)
            # 存储到datalist
            datalist.append(data)
    for aaa in datalist:
        # print(aaa)
        pass
    return datalist


# 得到一个指定url的网页内容
def askurl(url):
    # 伪造浏览器头部信息
    hea = {
        "Accept": "text/html,application xhtml+xml,application/xml;q=0.9,"
                  "image/avif,image/webp,image/apng,*/*;q = 0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        # 淦，坑系列，服务器传送数据为zip压缩格式，需浏览器算法内核解析
        # "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q = 0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }
    req = urllib.request.Request(url, headers=hea)
    html = ""
    try:
        # 二进制进行传参解码
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")  # "ignore"
        # print(html)
    except Exception as e:
        print("出现{0}".format(e))
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 创建数据库过程初始化
def init_db(dbpath):
    # 创建数据表
    sql = '''
        create table movie250(
         id integer primary key AUTOINCREMENT,
         cname message_text,
         ename message_text,
         link message_text,
         image_link message_text,
         pinfen varchar,
         renshu varchar,
         gaikuo varchar,
         info text
        );
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()  # 创建获取游标
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("数据库关闭啦。。。")


# 保存数据到excle
def savedata(datalist, dbpath):
    init_db(dbpath)
    # 打开数据库文件
    coon = sqlite3.connect(dbpath)
    # 创建游标结果集
    cur = coon.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250(cname, ename, link, image_link, pinfen, renshu, gaikuo, info)
            values(%s)''' % ",".join(data)
        print(sql)
        cur.execute(sql)
        coon.commit()
    cur.close()
    coon.close()


if __name__ == '__main__':
    baseurl = "https://movie.douban.com/top250?start"
    # 爬取网页
    datalist = getdata(baseurl)
    # 指定数据库
    dbpath = "movie.db"
    # 保存数据到数据库
    savedata(datalist, dbpath)
