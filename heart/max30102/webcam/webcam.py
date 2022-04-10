import os
import sys
import re
import requests
import time
import json
import pyttsx3

def tts(text):
    engine = pyttsx3.init()
    engine.setProperty('voice','zh')
    engine.say(text)        
    engine.runAndWait()

def TakeAPic(filename = "test.jpg"):
    path = ""
    os.system("fswebcam --no-banner -S 20 -r 1920x1080 " + filename)
    
def sendAPic(filename = "test.jpg"):
    
    url = "http://59.127.131.152:8080"
    f=open(filename,'rb')
    files = {'file':f}
    r = requests.post(url=url,files=files)

    print(r.text)
    os.remove(filename)
    result = json.loads(r.text)
    return result

def main():
    
    # default
    filename = "default"
    
    localtime = time.localtime()
    filename = time.strftime("img_%Y%m%d%I%M%S.jpg",localtime)
    print("filename=",filename)
    
    TakeAPic(filename)
    result = sendAPic(filename)
    if result['status'] == 0:
        tts('前方號誌為')
        
        if result['data'] == 'Sign':
            print(result['data'])
            tts('一般紅綠燈的')
        elif result['data'] == 'Psign':
            print(result['data'])
            tts('行人號誌燈的')
        else:
            print('無法辨識')
            tts('無法辨識')
        
        if result['data2'] == 'red':
            print(result['data2'])
            tts('紅燈')
        elif result['data2'] == 'green':
            print(result['data2'])
            tts('綠燈')
        else:
            print('無法辨識')
            tts('無法辨識')
    else:
        print('無法辨識')
        tts('無法辨識')