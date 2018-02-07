#! python3.3.3
# coding:utf-8
import urllib.request
import random
import time
import re

# url = "http://www.dianping.com/shop/16991821"

user_agent_headers = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
]

referer_headers = [
    "http://www.dianping.com/tianjin",
    "http://www.dianping.com/beijing",
    "http://www.dianping.com/wuhan",
    "http://www.dianping.com/shanghai",
    "http://www.dianping.com/chongqing",
    "http://www.dianping.com/hangzhou",
    "http://www.dianping.com/chengdu",
    "http://www.dianping.com/guangzhou",
    "http://www.dianping.com/xian",
    "http://www.dianping.com/nanjing",
    "http://www.dianping.com/suzhou"
]

proxy_host_list = []  # 定义可用的代理ip

def get_content(url):
    random_agent_header = random.choice(user_agent_headers)
    random_referer_header = random.choice(referer_headers)

    req = urllib.request.Request(url)
    req.add_header("User-Agent", random_agent_header)
    req.add_header("Host", "www.dianping.com")
    req.add_header("Referer", random_referer_header)
    req.add_header("GET", url)

    """
    ## 使用ip代理时打开
    proxy_host = random.choice(proxy_host_list)
    proxy_temp = {"http": proxy_host}
    proxy_support = urllib.request.ProxyHandler(proxy_temp)
    opener = urllib.request.build_opener(proxy_support)
    # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
    urllib.request.install_opener(opener)
    #res = urllib.request.urlopen(url).read().decode('utf-8')
    """

    return urllib.request.urlopen(req).read().decode('utf-8')

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

def get_proxy_ip_from_server(server_url):
    """
    获取服务返回的代理ip地址
    :param server_url:
    :return:
    """
    ip_str = get_content(server_url)
    return ip_str.split(',')

def get_proxy_ip_from_local_file(local_url):
    """
    获取文件中的URL，并去掉行末的换行符
    :param local_url:
    :return:
    """
    ip_list = []
    fp = open(local_url, 'r')
    ip_tmp_list = fp.readlines()
    for x in ip_tmp_list:
        ip_list.append(x.strip())
    return ip_list

############# 主入口: ##########################
if __name__ == '__main__':

    ##### 常量定义 开始 #################
    num = 20000  # 要抓取的URL数量
    server_url = 'http://xxxxxxxxx'  # 获取代理ip的url
    local_url = 'C:\\xxxxxx\\xxxx'  # 本地存储代理ip的文件路径
    url_save_path = 'C:\\Users\\zengjia\\Desktop\\spider_url2.txt'
    seed_url = 'http://www.dianping.com/tianjin'  # 开始抓取的第一个URL
    ##### 常量定义 结束 #################

    ########## 获取代理ip地址 开始 ##############
    proxy_host_list = get_proxy_ip_from_server(server_url)
    if len(proxy_host_list) == 0:
        proxy_host_list = get_proxy_ip_from_local_file(local_url)

    ########## 获取代理ip地址 结束 ###############

    url_all = []
    content = get_content(seed_url)
    url_list = get_url_from_content(content)
    url_all.extend(url_list)
    url_all = list(set(url_all))  # 去重

    i = 0
    n = 20  # 每20条URL向文件保存一次
    index = 0
    while i < len(url_all):
        url = url_all[i]
        try:
            content = get_content(url)
            url_list = get_url_from_content(content)
            url_all.extend(url_list)
            url_all = get_unique_merge(url_all, url_list)  # 去重并合并

            if len(url_all) >= num:
                break
        except Exception as e:
            pass

        i = i + 1
        if i % n == 0:
            url_list_temp = url_all[index * n: (index + 1) * n]
            index += 1
            save_to_file(url_list_temp, url_save_path)

        print(len(url_all))
        time.sleep(4)

    url_list_temp = url_all[index * n:]
    save_to_file(url_list_temp, url_save_path)
