#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/15 22:14
# @Author  : ChenHuan
# @Site    : 
# @File    : spider.py
# @Desc    :
# @Software: PyCharm
# 引入HTTP库
import requests
# 引入异常处理
from requests.exceptions import RequestException
# 引入re模块,和json模块
import re
import json
# 引入进程池
from multiprocessing import Pool
import time

def get_one_page(url):
    """获取HTML网页代码"""
    try:
        heasers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        response = requests.get(url, headers = heasers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """解析HTML网页代码"""
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">'
                         +'(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    # 采用 '+' 换行,re.S匹配任意字符这里主要是针对代码中的换行符
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
     with open('Maoyantop100.txt', 'a', encoding='utf-8') as f:
         # json.dumps将字典转换为字符串
         f.write(json.dumps(content, ensure_ascii=False) + '\n')
         f.close()

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for result in parse_one_page(html):
        write_to_file(result)

if __name__ == '__main__':
    print("开始抓取%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    print("结束抓取{}" .format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))