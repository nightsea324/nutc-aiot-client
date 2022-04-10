import max30102
import hrcalc
import statistics
from RPi import GPIO
import time
import requests
import os
from webcam import webcam

m = max30102.MAX30102()

hr2 = 0
lastheart = 0
lastspo2 = 0
sp2 = 0
heart = [60]
avgspo2 = [98]
checkhr = False
checksp = False
url = "http://59.127.131.152:8080"

GPIO.setmode(GPIO.BOARD)
buttonPin = 37
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
            webcam.main()
            f = open(filename, 'w+')
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
                        print('Heart Rate too high ->',lastheart)
                        f.write('Heart Rate too high ->'+str(lastheart)+"\n")
                        print(hr2)
                    heart.append(hr2)
                    print(hr2)
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
                        print('SPO2 too low ->',lastspo2)
                        f.write('SPO2 too low ->'+str(lastspo2)+"\n")
                        print(sp2)
                    heart.append(sp2)
                    print(sp2)
                #for i in range(10):
                    #avgspo2.append(sp2)
                #avgsp = statistics.mean(avgspo2)
                #print("SPO2       : ",sp2)
                #print('SPO2 avg : ',avgsp)
            if checksp == True and checkhr == True:
                print('情緒過於激動')
                f.write('情緒過於激動')
            f.close()
            

            f=open(filename,'rb')
            files = {'file':f}
            r = requests.post(url=url,files=files)
            
            print(r.text)
            os.remove(filename)
        

    prev_input = input
    time.sleep(0.05)


