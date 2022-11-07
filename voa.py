#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, arrow, os, datetime, json, requests, threading, urllib3
from lxml import etree
from urllib.parse import urlparse

now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD_HH:mm:ss')
dire = os.path.dirname(os.path.abspath(__file__))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# output_filename = os.path.join(dire, '/mp3/')
# if not os.path.exists(output_filename):
#     os.makedirs(output_filename)

def d(durl):
    open('/usr/local/app/mp3/'+os.path.basename(urlparse(durl).path),'wb').write(requests.get(durl).content)
    
if __name__ == "__main__":
    url = 'https://www.51voa.com/'
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    resp = requests.get(url, headers=header)
    html = etree.HTML(resp.text)
    xs = html.xpath("//div[@class='list']/ul/li")
    for x in xs:
        l = x.xpath("a[@class='lrc']")
        if len(l) == 1:
            a = x.xpath("a[last()]")[0]
            href = a.xpath("@href")[0]
            titl = a.xpath("text()")[0]
            cont = requests.get(url + href, headers=header)
            con = etree.HTML(cont.text)
            mp3 = con.xpath("//a[@id='mp3']/@href")
            lrc = con.xpath("//a[@id='lrc']/@href")
            print(titl)
            if len(mp3) != 0:
                d(mp3[0])
            if len(lrc) != 0:
                d(url+lrc[0])


# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# selenium webdriver_manager 
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
