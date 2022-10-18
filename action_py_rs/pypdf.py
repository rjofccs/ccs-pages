#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, arrow, os, time, json, fpdf, threading 
# from Crypto.Cipher import AES
# https://pyfpdf.readthedocs.io/en/latest/reference/cell/index.html

now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD_HH:mm:ss')
dire = os.path.dirname(os.path.abspath(__file__))
input_filename = os.path.join(dire, 'ielts_now.txt')
output_filename = os.path.join(dire, 'ielts_now.pdf')

# pdf
class PDF(fpdf.FPDF):
    def header(self):
        pass
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, str(self.page_no()) + '/{nb}', 0, 0, 'C')
        
def test_main():
    col_num = 9
    font_size = 10
    _w = 21
    _h = 6
    
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', font_size)
    
    para = []
    f = open(input_filename, 'r')
    lines = f.readlines()
    for line in lines:
        words = line.strip().split('|')
        ww = []
        for word in words:
            ww.append(word)
        para.append(ww)
        
    pn = 1
    for p in para:
        pdf.cell(_w, _h, 'No. '+str(pn), 0, 1)
        page = [p[i:i+col_num] for i in range(0, len(p), col_num)]
        for pg in page:
            i = 1
            for w in pg:
                pdf.cell(_w, _h, w, 1, 0, link = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/'+w.replace(' ','-'))
                i =  i + 1
            pdf.ln()
            left = col_num - len(pg)
        pn = pn + 1
#         pdf.ln(_h)
    pdf.output(output_filename, 'F')

if __name__ == "__main__":
    sing_thread = threading.Thread(target=test_main)
    sing_thread.start()





# cipher
# _file = dire+r'\T1.txt'
# _en = dire+r'\E'
# _pwd = "1234123412341234"

# with open(_file, "w") as f:
#     f.writelines('1')
#     print('1')

# file_in = open(_file, "rb")
# nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
# data = AES.new(bytes(_pwd, encoding='utf-8')[:16], AES.MODE_EAX, nonce).decrypt_and_verify(ciphertext, tag)
# open(_en, 'wb').write(data)
# file_in.close()
# os.remove(_file)

# cipher = AES.new(bytes(_pwd, encoding='utf-8')[:16], AES.MODE_EAX)
# ciphertext, tag = cipher.encrypt_and_digest(open(_en, 'rb').read())
# file_out = open(_file, "wb")
# [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
# file_out.close()

# with open(_file, "r") as f:
#     print(f.readlines())
