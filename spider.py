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

proxy_host_list = [] # 定义可用的ip

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

def get_soup(content):

    # 根据HTML网页字符串结构创建BeatifulSoup对象。
    soup = BeautifulSoup(content,  # HTML文档字符串
                         'lxml',  # HTML解析器 html.parser
                         from_encoding='utf-8'  # HTML文档编码
                         )
    # print(soup)
    return soup


def get_info(content): ## 美食店铺
    soup = get_soup(content)
    try:
        basic_info = soup.find_all('div', id='basic-info')
        if len(basic_info) == 0:
            basic_info = soup.find_all('div', class_='basic-info')
        basic_info = basic_info[0]

        breadcrumb = soup.find('div', class_='breadcrumb')

        ## 店铺名称
        try:
            shop_name = breadcrumb.find('span').get_text()
        except Exception as es:
            shop_name = basic_info.find('h1', class_='shop-name').get_text(strip=True)

        ## 地址
        address = basic_info.find('span', itemprop='street-address').get_text(strip=True)
        #print(address)

        ## 电话
        tel = basic_info.find('span', itemprop='tel').get_text(strip=True)
        #print(tel)

        info = shop_name + '\t' + address + '\t' + tel + '\n'

        print(info)
        return info
    except Exception as e:
        pass

def get_train_info(content): ## 培训类店铺
    soup = get_soup(content)
    try:
        breadcrumb = soup.find('div', class_='breadcrumb')
        ## 店铺名称
        shop_name = breadcrumb.find('div', class_='inner').find('span').get_text(strip=True)

        basic_info = soup.find_all('div', id='basic-info')
        if len(basic_info) == 0:
            basic_info = soup.find_all('div', class_='basic-info')
        basic_info = basic_info[0]

        address = basic_info.find('div', class_='address').get_text(strip=True)

        tel = basic_info.find('span', class_='item J-phone-hide')['data-phone']

        info = shop_name + '\t' + address + '\t' + tel + '\n'

        print(info)
        return info

    except Exception as e:
        pass

def get_train_info2(content): ## 培训类店铺
    soup = get_soup(content)
    try:
        breadcrumb = soup.find('div', class_='breadcrumb')
        ## 店铺名称
        shop_name = breadcrumb.find('span').get_text(strip=True)

        basic_info = soup.find_all('div', id='basic-info')
        if len(basic_info) == 0:
            basic_info = soup.find_all('div', class_='basic-info')
        basic_info = basic_info[0]

        address = basic_info.find('div', class_='address').get_text(strip=True)

        tel = basic_info.find('span', class_='item J-phone-hide')['data-phone']

        info = shop_name + '\t' + address + '\t' + tel + '\n'

        print(info)
        return info

    except Exception as e:
        pass


def get_url_list_from_error_log(file_path):
    """
    从错误日志中提取出有用的url
    :param file_path:
    :return:
    """
    fp = open(file_path, 'r')
    error_list = fp.readlines()
    fp.close()
    reg = "http://www.dianping.com/shop/(\d+)"
    pettern = re.compile(reg)
    url_list_from_log = []
    for line in error_list:
        try:
            shop_id = pettern.search(line).groups()[0]
            temp_url = 'http://www.dianping.com/shop/' + shop_id
            url_list_from_log.append(temp_url)
        except Exception as e:
            pass

    return list(set(url_list_from_log))

def get_proxy_ip():
    '''''
    获取网站中代理IP地址
    '''
    proxy = []
    for i in range(1, 2):
        try:
            url = 'http://www.xicidaili.com/nn/' + str(i)
            req = urllib.request.Request(url, headers={})
            res = urllib.request.urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(res,
                                 'lxml',  # HTML解析器 html.parser
                                 from_encoding='utf-8'  # HTML文档编码
                                 )
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                proxy.append(ip_temp)

        except Exception as e:
            continue
    return validate_ip(proxy)

def validate_ip(proxy):
    '''''
    验证获得的代理IP地址是否可用
    '''
    result_ips = []
    url = "http://ip.chinaz.com/getip.aspx"
    socket.setdefaulttimeout(2)
    for i in range(0, len(proxy)):
        try:
            ip = proxy[i].strip()
            proxy_host = "http://" + ip
            proxy_temp = {"http": proxy_host}
            proxy_support = urllib.request.ProxyHandler(proxy_temp)
            opener = urllib.request.build_opener(proxy_support)
            # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
            urllib.request.install_opener(opener)
            res = urllib.request.urlopen(url).read()
            result_ips.append(ip)
            print(proxy[i])
        except Exception as e:
            continue

    return result_ips

############# 主入口: ##########################
if __name__ == '__main__':

    ## 常量定义
    #error_log = 'C:\\Users\\zengjia\\Desktop\\error.txt'  # 定义错误日志路径
    #url_path = 'C:\\Users\\zengjia\\Desktop\\url_back.txt'  # 定义url路径
    shop_info_path = 'C:\\Users\\zengjia\\Desktop\\shop-info3.txt'  # 定义结果文件路径
    url_all_path = 'C:\\Users\\zengjia\\Desktop\\url2.txt'  # 定义URL文件路径
    forbiden_url_path = 'C:\\Users\\zengjia\\Desktop\\forbiden_url.txt'  # 定义访问失败的url保存路径

    ## 对url_all中的url进行抓取
    f = open(url_all_path,'r')
    url_list = f.readlines()
    f.close()
    print(len(url_list))

    # 用来保存店铺信息
    fp = open(shop_info_path, 'a+', encoding='utf-8')

    # 用来保存抓取失败的url
    fpp = open(forbiden_url_path, 'a+', encoding='utf-8')

    """
    现在只支持两类店铺数据的抓取：
        1.餐饮类店铺，
        2.培训类店铺
    """
    for url in url_list:
        try:
            url = url.strip()
            content = get_content(url)
            #print(content)
            shop_info = get_info(content)
            if shop_info is not None and shop_info != '':
                fp.write(shop_info)
            else:
                shop_info = get_train_info(content)
                if shop_info is not None and shop_info != '':
                    fp.write(shop_info)
                else:
                    fpp.write(url + '\n')
                    fpp.flush()

        except Exception as e:
            fpp.write(url + '\n')
            fpp.flush()
            continue

        fp.flush()
        time.sleep(5)

    fp.close()
    fpp.close()
