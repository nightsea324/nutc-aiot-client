import max30102
import hrcalc
import statistics
import time
import requests
import os
from RPi import GPIO
import time

m = max30102.MAX30102()

hr2 = 0
lastheart = 0
lastspo2 = 0
sp2 = 0
heart = [60]
avgspo2 = [98]
checkhr = False
checksp = False

#with open("SPO2.txt","a") as f:

url = "http://59.127.131.152:8080"

GPIO.setmode(GPIO.BOARD)
buttonPin = 15
GPIO.setup(buttonPin,GPIO.IN)
prev_input = 1
while True:
    input = GPIO.input(buttonPin)
    if((not prev_input)and input):
        print("press")
    while True:
        
        localtime = time.localtime()
        filename = time.strftime("hrb_%Y%m%d%I%M%S.txt",localtime)
            red, ir = m.read_sequential()
            f = open(filename, 'w+')
            print("偵測不到資料")
            f.write('偵測不到資料'+"\n")
            hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)
          
            print("hr detected:",hrb)
            f.write("hr detected:"+str(hrb)+"\n")
            print("sp detected:",spb)
            f.write("sp detected:"+str(spb)+"\n")
                
            if(hrb == True and hr != -999):
                hr2 = int(hr)
                for i in range(1):
                    lastheart = heart.pop()
                    if (hr2-lastheart) >= 15:
                        checkhr = True
                        print('Heart Rate too high ->'+str(lastheart))
                        f.write('Heart Rate too high ->'+str(lastheart)+"\n")
                        print(hr2)
                        f.write(str(hr2)+"\n")
                    heart.append(hr2)
                    print(hr2)
                    f.write(str(hr2)+"\n")
                        #for i in range(10):
                            #avgheart.append(hr2)
                    #avghr = statistics.mean(avgheart)
                    #print("Heart Rate : ",hr2)
                    #print('avg heart : ',avghr)
                    #break
            if(spb == True and sp != -999):
                sp2 = int(sp)
                for i in range(1):
                    lastspo2 = heart.pop()
                    if sp2 <= 95 :
                        checksp = True
                        print('SPO2 too low ->'+str(lastspo2))
                        f.write('SPO2 too low ->'+str(lastspo2)+"\n")
                        print(sp2)
                        f.write(str(sp2)+"\n")
                    heart.append(sp2)
                    print(sp2)
                    f.write(str(sp2)+"\n")
                    #for i in range(10):
                        #avgspo2.append(sp2)
                    #avgsp = statistics.mean(avgspo2)
                    #print("SPO2       : ",sp2)
                    #print('SPO2 avg : ',avgsp)
             
            if checksp == True and checkhr == True:
                print('情緒過於激動')
                f.write('情緒過於激動'+"\n")
        
        f.close()
            
        f=open(filename,'rb')
        files = {'file':f}
        r = requests.post(url=url,files=files)
        print(r.text)
        os.remove(filename)
