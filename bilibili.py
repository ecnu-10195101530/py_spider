"""
目标：爬取b站视频

作者：王浩
日期：2022/6/2

环境：
    window10
    pycharm
    python3.8
    ffmpeg >>>  用于把音视频分开的数据合并

模块：
    requests
    re
    json
    pprint
    os
    subprocess

b站视频数据：
    1.音频
    2.视频

关键点：
    ffmpeg，
    headers.referer
    json_data
仅供学习交流使用

"""
import requests
import re
import json
import pprint  # 格式化输出
import os
import subprocess

filename = 'b站视频\\'
if not os.path.exists(filename):  # 在当前项目目录创建文件夹music用于爬取存储
    os.mkdir(filename)

def get_response(html_url):
    # 伪装并发送请求
    headers = {
        # 防盗链：假装从正规访问路径进行浏览
        'referer': 'https://www.bilibili.com',
        # 伪装从浏览器访问
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)
    return response


def get_video_info(html_url):
    response = get_response(html_url)
    title = re.findall('<title data-vue-meta="true">(.*?)</title>', response.text)[0]
    # 利用正则表达式，匹配的结果输出为一个列表,取第一个元素[0]
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]
    # 列表中每一个元素为字符串，利用json把字符串转字典
    json_data = json.loads(html_data)
    # pprint.pprint(json_data)
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']  #取返回列表中的第一个元素中的baseurl
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    info = [title, audio_url, video_url]
    return info


def save(title, audio_url, video_url):
    # 存储数据
    audio_content = get_response(audio_url).content
    video_content = get_response(video_url).content
    with open(filename+title+'.mp3', mode='wb') as f:
        f.write(audio_content)
    with open(filename+title+'.mp4', mode='wb') as f:
        f.write(video_content)
    print(f"--------------已完成：{title}--------------")


url = 'https://www.bilibili.com/video/BV1wD4y1o7AS'  # 目标url，跟据需求可以改为循环调用列表完成大量视频爬取
video_info = get_video_info(url)
save(video_info[0], video_info[1], video_info[2])
