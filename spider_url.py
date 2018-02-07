#! python3.3.3
# coding:utf-8
import urllib.request
import random
import time
import re
from bs4 import BeautifulSoup
import socket

#url = "http://www.dianping.com/shop/16991821"

user_agent_headers = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
    ]

def get_content(url, headers):

    random_header = random.choice(headers)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "www.dianping.com")
    req.add_header("Referer", "http://www.dianping.com/tianjin")
    req.add_header("GET", url)

    return urllib.request.urlopen(req).read().decode('utf-8')

def get_soup(content):
    # 根据HTML网页字符串结构创建BeatifulSoup对象。
    soup = BeautifulSoup(content,  # HTML文档字符串
                         'lxml',  # HTML解析器 html.parser
                         from_encoding='utf-8'  # HTML文档编码
                         )
    # print(soup)
    return soup

def get_url_from_content(content):
    """
    从content中正则匹配满足条件的URL
    :param content:
    :return:
    """
    result = []
    reg = "www.dianping.com/shop/(\d+)"
    pattern = re.compile(reg)
    ids = pattern.findall(content)
    ids_list = list(set(ids))
    for x in ids_list:
        url = 'http://www.dianping.com/shop/' + x
        result.append(url)
    return result

def get_unique_merge(url_all, url_list):
    """
    合并两个list并去重，保留元素的相对位置不变
    :param url_all:
    :param url_list:
    :return:
    """
    for url in url_list:
        if url not in url_all:
            url_all.append(url)
    return url_all

def save_to_file(url_list, file_path):
    """
    将URL保存到文件中
    :param url_list:
    :param file_path:
    :return:
    """
    fp = open(file_path, 'a+')
    for url in url_list:
        fp.write(url + '\n')
        fp.flush()
    fp.close()

############# 主入口: ##########################
if __name__ == '__main__':

    url_save_path= 'C:\\Users\\zengjia\\Desktop\\spider_url.txt'
    url_all = []
    content = get_content('http://www.dianping.com/tianjin', user_agent_headers)
    url_list = get_url_from_content(content)
    url_all.extend(url_list)
    url_all = list(set(url_all))  # 去重

    i = 0
    while i < len(url_all):
        url = url_all[i]
        try:
            content = get_content(url, user_agent_headers)
            url_list = get_url_from_content(content)
            url_all.extend(url_list)
            url_all = get_unique_merge(url_all, url_list)  # 去重并合并

            if len(url_all) >= 20000:
                save_to_file(url_all, url_save_path)
                break
        except Exception as e:
            pass

        i = i + 1
        print(len(url_all))
        time.sleep(5)

    if i == len(url_all):
        save_to_file(url_all, url_save_path)