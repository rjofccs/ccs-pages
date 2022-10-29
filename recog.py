# -*- coding: utf8 -*-
# pip install aliyun-python-sdk-core==2.13.3
import sys, arrow, os, time, tkinter, datetime, json, base64, threading
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

dire = os.path.dirname(os.path.abspath(__file__))
now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

def fileTrans(akId, akSecret, appKey, fileLink, num):
    client = AcsClient(akId, akSecret, "cn-shanghai")

    postRequest = CommonRequest()
    postRequest.set_domain("filetrans.cn-shanghai.aliyuncs.com")
    postRequest.set_version("2018-08-17")
    postRequest.set_product("nls-filetrans")
    postRequest.set_action_name("SubmitTask")
    postRequest.set_method('POST')
    task = {"appkey" : appKey, "file_link" : fileLink, "version" : "4.0", "enable_words" : True, "enable_sample_rate_adaptive": True}
    postRequest.add_body_params("Task", json.dumps(task))
    taskId = ""
    try :
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        print (postResponse)
        statusText = postResponse["StatusText"]
        if statusText == "SUCCESS" :
            print ("录音文件识别请求成功响应！")
            taskId = postResponse["TaskId"]
        else :
            print ("录音文件识别请求失败！")
            return
    except Exception as e:
        print (e)

    getRequest = CommonRequest()
    getRequest.set_domain("filetrans.cn-shanghai.aliyuncs.com")
    getRequest.set_version("2018-08-17")
    getRequest.set_product("nls-filetrans")
    getRequest.set_action_name("GetTaskResult")
    getRequest.set_method('GET')
    getRequest.add_query_param("TaskId", taskId)
    statusText = ""
    while True :
        try :
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            print (getResponse)
            statusText = getResponse["StatusText"]
            if statusText == "RUNNING" or statusText == "QUEUEING" :
                time.sleep(10)
            else :
                break
        except Exception as e:
            print (e)
    if statusText == "SUCCESS" :
        print ("录音文件识别成功！")
        words = getResponse['Result']['Words']
        f = open(dire+'\\'+num+'.txt','w')
        lastEnd=0
        for word in words:
            if word['ChannelId']==0:
                t = int(word['BeginTime'])-lastEnd
                if t>1000:
                    f.writelines('.\n')
                else:
                    f.writelines(' ')
                f.writelines(''+word['Word'])
                
                # print(t, word['Word'])
                lastEnd=int(word['EndTime'])
        f.writelines('.')
    else :
        print ("录音文件识别失败！")


fileLink = "https://down.guixue.com/mp3/ielts_lexicon/.mp3"
fileTrans(accessKeyId, accessKeySecret, appKey, fileLink, num)
