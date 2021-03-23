# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@ Author ：Lan
@ blog ：www.lanol.cn
@ Date ： 2020/12/19
@ Description：I'm in charge of my Code
-------------------------------------------------
"""
import parsel
import requests
import threading


def getContet(urls):
    for i in urls:
        url = 'https://www.qinghuawang.net/' + i
        res = requests.get(url).content
        res = res.decode("gb2312", errors='ignore')
        xpath = parsel.Selector(res)
        content = xpath.xpath("//p/text()").extract()
        with open('sentence.txt', 'a+', encoding='utf8') as f:
            for j in content:
                f.write(j + "\n")
                print(j)


def getAll():
    for i in range(1, 20):
        url = f'https://www.qinghuawang.net/qinghua/list_1_{i}.html'
        res = requests.get(url).content
        xpath = parsel.Selector(res.decode('gb2312'))
        urlList = xpath.xpath("//li/a[@class='articleTitle fl']/@href").extract()
        threading.Thread(target=getContet, args=(urlList,)).start()


if __name__ == '__main__':
    getAll()