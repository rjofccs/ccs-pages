# -*- coding: utf8 -*-
# pip install aliyun-python-sdk-core==2.13.3
'''
{
	"Words": [{
		"Word": "facebook",
		"EndTime": 1099,
		"BeginTime": 0,
		"ChannelId": 0
	}, {
		"Word": "parent",
		"EndTime": 1832,
		"BeginTime": 1099,
		"ChannelId": 0
	}],
	"Sentences": [{
		"EndTime": 13930,
		"SilenceDuration": 0,
		"BeginTime": 0,
		"Text": "facebook parent company. meta has built a technology tool designed to directly translate spoken speech from one language to another. ",
		"ChannelId": 0,
		"SpeechRate": 86,
		"EmotionValue": 7.3
	}, {
		"EndTime": 30740,
		"SilenceDuration": 0,
		"BeginTime": 14460,
		"Text": "meta recently released a video that demonstrated how the artificial intelligence ai powered tool can translate between english and the hokkien language. ",
		"ChannelId": 0,
		"SpeechRate": 81,
		"EmotionValue": 7.2
	}]
}
'''
import sys, arrow, os, time, datetime, json, base64, threading
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

dire = os.path.dirname(os.path.abspath(__file__))
now = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

def fileTrans(akId, akSecret, appKey, fileLink, fileName):
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
            resp = client.do_action_with_exception(getRequest)
            resp = json.loads(resp)
            print (resp)
            statusText = resp["StatusText"]
            if statusText == "RUNNING" or statusText == "QUEUEING" :
                time.sleep(10)
            else :
                break
        except Exception as e:
            print (e)
    if statusText == "SUCCESS" :
        print ("录音文件识别成功！")
        # res = resp['Result']
        # f.write(json.dumps(res))
        
        f = open('/usr/local/www/html/'+fileName,'w')
        sens = resp['Result']['Sentences']
        for sen in sens:
            if sen['ChannelId']==0:
                begin = int(sen['BeginTime'])
                end = int(sen['EndTime'])
                f.writelines('{}--{}=={}\n'.format(begin,end,sen['Text']))
    else :
        print ("录音文件识别失败！")


appKey = "O7PwMh9AZEdSsMVt"
fileLink = "https://files.51voa.cn/202210/meta-demonstrates-ai-powered-speech-to-speech-translation-system.mp3"
fileTrans(accessKeyId, accessKeySecret, appKey, fileLink, 'test.txt')
