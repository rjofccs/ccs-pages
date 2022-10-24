# -*- coding: utf8 -*-
import sys, arrow, os, shutil, time, json, base64, requests, re
from lxml import etree
# from selenium import webdriver


dire = os.path.dirname(os.path.abspath(__file__))
now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
domain = 'https://dictionary.cambridge.org'
ua = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"

def make_cn_http(word):
    url = domain + '/dictionary/english-chinese-simplified/' + word
    resp = requests.get(url, headers={'User-Agent': ua})
    return resp.text
#     opt = webdriver.ChromeOptions()
#     opt.headless = True
#     browser = webdriver.Chrome(options = opt)
#     browser.get(url)
#     html = browser.page_source
#     return html


def make_en_http(word):
    url = domain + '/dictionary/english/' + word
    resp = requests.get(url, headers={'User-Agent': ua})
    return resp.text

def print_html(xhtml):
    shtml = etree.tostring(xhtml).decode('utf-8')
    print(shtml)

def get_multi_xpath(xhtml, sxpath):
    shtml = etree.tostring(xhtml).decode('utf-8')
    parse_html = etree.HTML(shtml)
    x = parse_html.xpath(sxpath)
    return x

def get_one_xpath(xhtml, sxpath):
    return get_multi_xpath(xhtml, sxpath)[0]

#查单词
def do_query(word):
    en_version = False
    try:
        html = make_cn_http(word.replace(' ','-'))
        parse_html = etree.HTML(html)
        xbody = get_one_xpath(parse_html, '//div[@class="entry-body"]')
    except:
        html = make_en_http(word.replace(' ','-'))
        parse_html = etree.HTML(html)
        xbody = get_one_xpath(parse_html, '//div[@class="entry-body"]')
        en_version = True
    # 多个词性
    xdd_list = get_multi_xpath(xbody, '//div[@class="pr entry-body__el"]')
    mean = []
    for dd in xdd_list:
        pos_data = {}
        # 一个pos-header furious多个
        pos_headers = get_multi_xpath(dd, '//div[@class="pos-header dpos-h"]')
        if len(pos_headers)>1:
            print(word)
        pos_header = pos_headers[0]
        pronoun = ''
        try:
            pronoun = get_one_xpath(pos_header, '//span[@class="pos dpos"]/text()')
        except:
            pass
        mp3s = get_multi_xpath(pos_header, '//source[@type="audio/mpeg"]/@src')
        pos_data['noun'] = pronoun
        prons = []
        for mp3 in mp3s:
            prons.append(domain + mp3)
        pos_data['prons'] = prons
        # 一个pos-body 多个意思
        trans = []
        if not en_version:
            dsenses = get_multi_xpath(dd, '//div[@class="def-body ddef_b"]')
            for dsense in dsenses:
                trans.append(get_one_xpath(dsense, '//span/text()'))
        else:
            dsenses = get_multi_xpath(dd, '//div[@class="def ddef_d db"]')
            pattern = re.compile(r'<.*?>')
            for dsense in dsenses:
                shtml = etree.tostring(dsense).decode('utf-8')
                out = re.sub(pattern, '', shtml).strip()
                trans.append(str(out))
        pos_data['trans'] = trans
        mean.append(pos_data)
    return json.dumps(mean)

#写html
def txt_append(fina, word, con):
    input_filename = os.path.dirname(dire)+'/esthetic/' + fina + '.html'
    if not os.path.exists(input_filename):
        pre = '''<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link href="./tailwind.css" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="./esthetic.css">
<script src="./esthetic.js"></script>
<script>const chapter = \''''+fina+'''\';</script>
</head>
<body>
    
<div class="nav">
    <a href="./index.html">Index</a>
    <a href="#/" onclick="hide(this);">Hide</a>
    <a href="#/" onclick="play(this);">Play</a>
    <a href="#/" onclick="next(this);">Next</a>
</div>
'''
        with open(input_filename, 'a') as f:
            f.write(pre+'\n')
    with open(input_filename, 'a') as f:
        f.write(con+'\n')
#读esthetic2
def read_file():
    para = []
    input_filename = os.path.join(dire, 'esthetic2.txt')
    f = open(input_filename, 'r')
    lines = f.readlines()
    for tline in lines:
        line = tline.strip()
        word = ''
        if line:
            pp = line.split(' == ')
            chapter = pp[0][:2]
            word = pp[1]
            js = json.loads(pp[2])

            mean = '''<div class="content">
    <div class="word" data-word="{}">{}<div class="mark" onclick="mark('{}')">Mark</div></div>
'''.format(word, word, word)
            size = len(js)
            for k in range(size):
                j = js[k]
                t = ''
                trans = j['trans']
                if len(trans)>0:
                    t = '✓ '.join([str(c) for c in trans])
                p = ''
                if len(j['prons'])>0:
                    # fetch first uk
                    aud = j['prons'][0]
                    ind = aud.find('pron/')
                    p = '    <p onclick="play_one(this)">{}<audio preload="none"><source src="{}"></audio>{}</p>'.format(j['noun'], './mp3/'+aud[ind-3:].replace('/','_'), t)
                mean = mean + p + ('\n' if k<(size-1) else '')
            mean = mean + '''
</div>'''
        txt_append(chapter, word, mean)
    txt_append(chapter, word, '''</body>
</html>''')

#下载mp3
def down_mp3():
    para = []
    input_filename = os.path.join(dire, 'esthetic2.txt')
    fr = open(input_filename, 'r')
    lines = fr.readlines()
    for tline in lines:
        line = tline.strip()
        if line:
            try:
                pp = line.split(' == ')
                js = json.loads(pp[2])
                for j in js:
                    for p in j['prons']:
                        doc = requests.get(p, headers={'User-Agent': ua})
                        ind = p.find('pron/')
                        with open(os.path.dirname(dire)+'/esthetic/mp3/'+p[ind-3:].replace('/','_'), 'wb') as fw:
                            fw.write(doc.content)
            except:
                print(pp[0]+' == '+pp[1])

#读esthetic2 一个mp3
def read_est():
    para = []
    input_filename = os.path.join(dire, 'esthetic2.txt')
    f = open(input_filename, 'r')
    lines = f.readlines()
    for tline in lines:
        line = tline.strip()
        if line:
            pp = line.split(' == ')
            if pp[2].strip() != '[]':
                chapter = pp[0][:2]
                word = pp[1]
                js = json.loads(pp[2])
                t = ''
                n = ''
                p = ''
                # fetch first mean
                if len(js)>0:
                    n = js[0]['noun']
                    if len(js[0]['trans'])>0:
                        t = '✓ '.join([str(c) for c in js[0]['trans']])
                    if len(js[0]['prons'])>0:
                        # fetch first uk
                        aud = js[0]['prons'][0]
                        ind = aud.find('pron/')
                        p = aud[ind-3:].replace('/','_')
                para.append((chapter, word, n, t, p))
    return para

#合并mp3
def con_est(ch):
    es = read_est()
    for obj in es:
        chapter, word, n, t, p = obj
        if int(chapter) == ch and word!='pictograph' and p:
            input_filename = os.path.dirname(dire)+'/esthetic/ff' + chapter + '.txt'
            with open(input_filename, 'a') as f:
                f.write('file \'mp3/'+p+'\'\n')
    # os.makedirs('./esthetic/mp4/')
    ii = str(ch).rjust(2, '0')
    os.system('ffmpeg -y -f concat -safe 0 -i ./esthetic/ff'+ii+'.txt -c copy ./esthetic/mp4/'+ii+'.mp3')
    os.remove(os.path.dirname(dire)+'/esthetic/ff' + ii + '.txt')

#es ielts_now2
def noo_est():
    input_filename = os.path.join(dire, 'ielts_now2.md')
    f = open(input_filename, 'r')
    lines = f.readlines()
    i = 0
    es = read_est()
    for tline in lines:
        i = i + 1
        if i<=22:
            ws = tline.strip('-').strip().split(', ')
            for w in ws:
                have = False
                for obj in es:
                    chapter, word, n, t, p = obj
                    if int(chapter) == i and word==w:
                        have = True
                if not have:
                    print(w)


if __name__ == '__main__':
    #     line = tline.strip()
    #     pp = line.split(': ')
    #     fina = pp[0][:2]
    #     word = pp[1]
    #     do_query(word)

    for i in range(22):
        ii = str(i+1).rjust(2, '0')
        os.remove(os.path.dirname(dire)+'/esthetic/' + ii + '.html')
    read_file()
    # down_mp3()
    # con_est(8)
    pass

