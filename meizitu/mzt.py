# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   URL：     www.meizitu.com
   Description :  meizitu的爬虫项目
   Author :        wuxier:Lowell Dardy
   date：          2020/2/24
-------------------------------------------------
   Change Activity:
                   2020/2/24: meizitu的爬虫项目
-------------------------------------------------
"""
__author__ = 'github_wuxier'

import requests
from bs4 import BeautifulSoup
import os
import time

def get_proxy():
    """
    获取代理
    代理使用的是jhao104大佬的proxy_pool项目docker搭建
    项目地址：https://github.com/jhao104/proxy_pool
    """
    proxyget_url = "http://106.12.51.245:5010/get/"
    return requests.get(proxyget_url).json()

#删除代理
def delete_proxy(proxy):
    """
    删除代理
    代理使用的是jhao104大佬的proxy_pool项目docker搭建
    项目地址：https://github.com/jhao104/proxy_pool
    """
    proxydel_url = "http://106.12.51.245:5010/delete/?proxy={}"
    requests.get(proxydel_url.format(proxy))

def get_html(url):
    """
    使用代理获取www.meizitu.com页面
    """
    retry_count = 5
    proxy = get_proxy().get("proxy")
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    while retry_count > 0:
        try:
            res = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            # 使用代理访问
            if res.status_code == 200:
                response = res.content
                return response
            else:
                return False
        except Exception:
            retry_count -= 1
    #出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

def parser_html(html):
    """
    页面解析，获取文件夹名file_name;图片链接数据imgs;
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        file_name = soup.select('div.metaRight a')[0].text
        imgs = soup.select('div p img')
        return file_name, imgs
    except:
        return False

def pic_path(file_name):
    """
    图片的存储路径
    win：F:\meizitu\
    linux：/home/meizitu
    """
    if (os.name == 'nt'):
        path = 'F:\meizitu\\'
        imgs_path = path + file_name
        creade_dir(imgs_path)
        print(u'你正在使用win平台,存储路径：' + imgs_path)
    else:
        path = '/home/meizitu/'
        imgs_path = path + file_name
        creade_dir(imgs_path)
        print(u'你正在使用linux平台,存储路径：' + imgs_path)

def pic_get(imgs, p_img):
    """
    获取图片的URL和name
    """
    img_url = imgs[p_img].get('src')
    img_name = img_url.split(r'/')[-1]
    return img_url, img_name


def pic_save(img_url, img_name):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    pic_res = requests.get(img_url, headers=headers)
    if pic_res.status_code == 200:
        response = pic_res.content
    else:
        return False
    if not os.path.exists(img_name):
        print(f'正在爬取{img_name}')
        with open(img_name, 'wb') as f:
            f.write(response)
        print(f'已完成{img_name}的爬取')
    else:
        print(f'已存在{img_name}')


def creade_dir(imgs_path):
    """
    创建文件夹
    如果不存在则创建目录,创建目录操作函数
    如果目录存在则不创建，并提示目录已存在
    """
    if not os.path.exists(imgs_path):
        os.makedirs(imgs_path)
        os.chdir(imgs_path)
        print(imgs_path + ' 创建成功')
        return True
    else:
        print(imgs_path + ' 目录已存在')
        os.chdir(imgs_path)
        return False

def main(num):
   """
   url为妹子图套图URL
   """
   url = f'https://www.meizitu.com/a/{num}.html'
   html = get_html(url)
   file_name = parser_html(html)[0]
   imgs = parser_html(html)[1]
   pic_path(file_name)
   for p_img in range(len(imgs)):
        img_url = pic_get(imgs, p_img)[0]
        img_name = pic_get(imgs, p_img)[1]
        print(img_name)
        print(img_url)
        pic_save(img_url, img_name)

if __name__ == '__main__':
    for i in range(1, 3):
        print(f'当前正在爬取第{i}套图')
        main(i)
        time.sleep(2)