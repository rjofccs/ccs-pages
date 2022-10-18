#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, arrow, os, time, json, threading

now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD_HH:mm:ss')
dire = os.path.dirname(os.path.abspath(__file__))
input_filename = os.path.join(dire, 'pass.txt')
output_filename = os.path.join(dire, 'pass.pdf')


def test_main():
    pass

if __name__ == "__main__":
    sing_thread = threading.Thread(target=test_main)
    sing_thread.start()
