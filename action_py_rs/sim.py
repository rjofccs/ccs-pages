# -*- coding: utf8 -*-
import os, json, re
dire = os.path.dirname(os.path.abspath(__file__))

para = []
input_filename = os.path.join(dire, 'esthetic2.txt')
output_filename = os.path.join(dire, 'esthetic5.json')
for tline in open(input_filename, 'r').readlines():
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
                    p = 'https://raw.githubusercontent.com/rjofccs/ccs-pages/master/esthetic/mp3/' + aud[ind-3:].replace('/','_')
            para.append((chapter, word, n, t, p))


open(output_filename, 'w').write(json.dumps(para))
