"""
目标：爬取网易云热歌榜

作者：王浩
日期：2022/6/2

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

import requests
import re  # 正则表达式
import os  # 文件操作

filename = 'music\\'
if not os.path.exists(filename):  # 在当前项目目录创建文件夹music用于爬取存储
    os.mkdir(filename)

url = "https://music.163.com/discover/toplist"

# 把python伪装成浏览器
headers = {
     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
# print(response.text)
html_data = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a>', response.text)  # 用正则表达式匹配得到的html
for music_id, title in html_data:
    music_url = f'https://music.163.com/song/media/outer/url?id={music_id}.mp3' #播放链接
    music_content = requests.get(url=music_url, headers=headers).content  # 访问url获取二进制文件
    with open(filename+title+'.mp3', mode='wb') as f:
        f.write(music_content)
    print(music_id, title)
