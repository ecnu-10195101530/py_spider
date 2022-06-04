"""
目标：爬取某墙纸网站

作者：王浩
日期：2022/6/3

环境：
    window10
    pycharm
    python3.8

模块：
    requests
    re
    os

仅供学习交流使用
"""
import os
import pprint
import requests
import re


filename = 'wallhaven\\'
if not os.path.exists(filename):  # 在当前项目目录创建文件夹music用于爬取存储
    os.mkdir(filename)

# https://w.wallhaven.cc/full/1k/wallhaven-1ky673.png 照片对象网址
url = 'https://wallhaven.cc/search?q=sky'
# 照片列表网站


def get_response(html_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)
    return response


response = get_response(url)
data = re.findall("data-href=\"https://wallhaven.cc/wallpaper/fav/(.*?)\"",response.text)


for title in data:
    pic_url = f'https://w.wallhaven.cc/full/{title[0]}{title[1]}/wallhaven-{title}.jpg'
    pic_content = get_response(pic_url).content
    with open(filename+title+'.jpg', mode='wb') as f:
        f.write(pic_content)
    print(title)

