# -*- coding: UTF-8 -*-
import requests,json
h={ 'X-Auth-PSK': '1234'}
d={
  'method': "setAudioVolume",
  'version': "1.2",
  'id': 1,
  'params': [{
        "volume": "5",
        "ui": "on",
        "target": "speaker"
    }]
}
resp=requests.post('http://192.168.0.101/sony/audio',headers=h,data=json.dumps(d))
# d={
#     "method": "getSupportedApiInfo",
#     "id": 5,
#     "params": [{"services": [
#         "system",
#         "avContent"
#     ]}],
#     "version": "1.0"
# }
# resp=requests.post('http://192.168.0.101/sony/guide',headers=h,data=json.dumps(d))
# j = json.loads(resp.content)
# for service in j['result'][0]:
#   for item in service['apis']:
#     print(item['name'])
# d={
#     "method": "setPowerStatus",
#     "id": 55,
#     "params": [{"status": True}],
#     "version": "1.0"
# }
# resp=requests.post('http://192.168.0.101/sony/system',headers=h,data=json.dumps(d))
# j = json.loads(resp.content)
# print(j)
# d={
#     "method": "getApplicationList",
#     "id": 60,
#     "params": [],
#     "version": "1.0"
# }
# resp=requests.post('http://192.168.0.101/sony/appControl',headers=h,data=json.dumps(d))
# j = json.loads(resp.content)
# for item in j['result'][0]:
#   print(item['title'],item['uri'])
d={
"method": "terminateApps",
"id": 55,
"params": [],
"version": "1.0"
}
# resp=requests.post('http://192.168.0.101/sony/appControl',headers=h,data=json.dumps(d))
# j = json.loads(resp.content)
# print(j)
d={
"method": "setActiveApp",
"id": 601,
"params": [{
"uri": "com.sony.dtv.com.xiaodianshi.tv.yst.com.xiaodianshi.tv.yst.ui.main.MainActivity"
}],
"version": "1.0"
}
# resp=requests.post('http://192.168.0.101/sony/appControl',headers=h,data=json.dumps(d))
# j = json.loads(resp.content)
# print(j)
d={
"method": "getRemoteControllerInfo",
"id": 54,
"params": [],
"version": "1.0"
}
resp=requests.post('http://192.168.0.101/sony/system',headers=h,data=json.dumps(d))
j = json.loads(resp.content)
for item in j['result'][1]:
    print(item['name'],item['value'])
# h={
# 'X-Auth-PSK': '1234',
# 'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
# 'Accept': '*/*',
# 'Connection': 'Keep-Alive',
# 'Content-Length': '313'
# }
# d='''
# <s:Envelope
# xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
# s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
# <s:Body>
# <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
# <IRCCCode>AAAAAQAAAAEAAAAVAw==</IRCCCode>
# </u:X_SendIRCC>
# </s:Body>
# </s:Envelope>
# '''
# resp=requests.post('http://192.168.0.101/sony/ircc',headers=h,data=d.encode('utf-8'))
# print(resp.content)

