# https://www.google.com.hk/search?tbm=isch&q=plateau
import sys, arrow, os, time, datetime, json, base64, threading, requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from urllib.parse import urlparse

dire = os.path.dirname(os.path.abspath(__file__))
now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

