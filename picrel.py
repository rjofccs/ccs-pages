#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, arrow, os, datetime, json, requests, threading, urllib3
from lxml import etree
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# selenium webdriver_manager 

now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD_HH:mm:ss')
dire = os.path.dirname(os.path.abspath(__file__))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
output_filename = os.path.join(dire, '/tmp/')
if not os.path.exists(output_filename):
    os.makedirs(output_filename)


# if __name__ == "__main__":
url = 'https://www.google.com.hk/search?tbm=isch&q='+'plateau'
# resp = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"})
# parse_html = etree.HTML(resp.text)
# xs = parse_html.xpath("//div[@id='islmp']")
# for x in xs:
#     img = x.xpath('a/div[2]/@style')[0].replace("background-image: url('",'').replace("')",'')

# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
# options.add_argument('window-size=1920x3000') # 指定浏览器分辨率
# options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
# options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
# options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
# options.add_argument('--headless')  #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
# driver.get(url)

# driver.save_screenshot('./ch.png')
# driver.quit()
