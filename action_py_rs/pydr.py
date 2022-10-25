#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, arrow, os, datetime, json, requests, threading, urllib3
from lxml import etree

now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD_HH:mm:ss')
dire = os.path.dirname(os.path.abspath(__file__))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
output_filename = os.path.join(dire, '/dr/tmp/')
if not os.path.exists(output_filename):
    os.makedirs(output_filename)


if __name__ == "__main__":
    # download('jiuse', str(sys.argv[1]))
os.remove('./index.html')
with open('./index.html', 'a') as f:
    for i in range(10):
        url = 'https://.com/author/%E5%8C%BF%E5%90%8D?page='+str(i+1)
        resp = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"})
        parse_html = etree.HTML(resp.text)
        xs = parse_html.xpath('//div[@class="video-elem"]')
        for x in xs:
            img = x.xpath('a/div[2]/@style')[0].replace("background-image: url('",'').replace("')",'')
            visit = x.xpath('small/div[@class="text-muted"]/text()[last()]')[1][10:]#.replace('\xa0|xa0','').replace('\n','').replace('次播放','').replace('万','w')
            # print(img, visit)
            f.write('<div>{}<img src="{}" onclick="window.open(this.src)" width="214" height="128"></div>\n'.format(visit, img))


def download(domain, id):
    for i in range(99):
        ts_url = "https://cdn.{}.cloud/hls/{}/index{}.ts".format(domain, id, i+1)
        file_name = ts_url.split("/")[-1]
        print("Downloading %s" %file_name)
        try:
            response = requests.get(ts_url,stream=True,verify=False)
            leaf = response.headers['Content-Length']
            if leaf =='555' or leaf =='146':
                return
        except Exception as e:
            print("Exception %s"%e.args)
            return
        ts_path = output_filename + str(i+1).rjust(2, '0') + ".ts"
        with open(ts_path,"wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    file_list = file_walker(output_filename)
    with open(os.path.join(dire, '/ts/'+id+'.ts'), 'wb+') as fw:
        for item in file_list:
            fw.write(open(item, 'rb').read())
    del_file(output_filename)

def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    return file_list

def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)