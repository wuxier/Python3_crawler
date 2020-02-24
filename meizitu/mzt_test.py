import requests
from bs4 import BeautifulSoup
import os
import time

if (os.name == 'nt'):
    path = 'F:\爬虫存储\meizitu\\'
    print(u'你正在使用win平台,存储路径为'+path)
else:
    path = '/home/meizitu/'
    print(u'你正在使用linux平台,存储路径为'+path)
#URL为1到9的套图URL
for i in range(1,10):
	url = f'https://www.meizitu.com/a/1.html'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
res = requests.get(url, headers=headers)
if res.status_code==200:
    response = res.content
    soup = BeautifulSoup(response, 'lxml')
    file_name = soup.select('div.metaRight a')[0].text
    imgs = soup.select('div p img')
#    print(file_name)
    imgs_path = path + file_name
    # 判断结果
    if not os.path.exists(imgs_path):
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(imgs_path)
        os.chdir(imgs_path)
        print(imgs_path + ' 创建成功')
        # return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        os.chdir(imgs_path)
        print(imgs_path + ' 目录已存在')
        # return False
    print(f'开始爬取{file_name}')
    for i in range(len(imgs)):
        pic_url = imgs[i].get('src')
        pic_name = pic_url.split(r'/')[-1]
        print(f'正在爬取{pic_name}')
        pic_get = requests.get(pic_url, headers=headers)
        with open(pic_name, 'wb') as f:
            f.write(pic_get.content)
        print(f'已完成{pic_name}的爬取')
        time.sleep(2)
    # return response
else:
    # return False
    print("dead")
