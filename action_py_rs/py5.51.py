# -*- coding: utf8 -*-
import sys, arrow, os, shutil, time, json, base64, requests, re, ffmpeg
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
                tran = ''
                noun = ''
                pron = ''
                # fetch first mean
                if len(js)>0:
                    noun = js[0]['noun']
                    if len(js[0]['trans'])>0:
                        tran = ''.join([str(c) for c in js[0]['trans']])
                    if len(js[0]['prons'])>0:
                        # fetch first uk
                        aud = js[0]['prons'][0]
                        ind = aud.find('pron/')
                        pron = 'https://github.com/rjofccs/ccs-pages/raw/master/esthetic/mp3/' + aud[ind-3:].replace('/','_')
                # para.append((chapter, word, noun, tran, pron))
                para.append((word, pron))
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
    est = read_est()
    output_filename = os.path.join(dire, 'esthetic4.json')
    f = open(output_filename, 'w')
    f.write(json.dumps(est))
    # con_est(8)
