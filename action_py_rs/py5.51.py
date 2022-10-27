# -*- coding: utf8 -*-
import sys, arrow, os, shutil, time, json, base64, requests, re
from lxml import etree
# from selenium import webdriver


dire = os.path.dirname(os.path.abspath(__file__))
now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')


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
                        t = ''.join([str(c) for c in js[0]['trans']])
                    if len(js[0]['prons'])>0:
                        # fetch first uk
                        aud = js[0]['prons'][0]
                        ind = aud.find('pron/')
                        p = aud[ind-3:].replace('/','_')
                para.append((chapter, word, n, t, p))
    return para

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

if __name__ == '__main__':
    read_file()
    # con_est(8)
