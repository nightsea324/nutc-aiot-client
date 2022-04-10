import max30102
import hrcalc
import statistics
import threading
import os
import serial
import time
import struct
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from threading import Thread
import RPi.GPIO as GPIO
from matplotlib.figure import Figure
import numpy as np

import datetime
from mmWave import peopleMB

from tkinter import *


m = max30102.MAX30102()

hr2 = 0
lastheart = 0
lastspo2 = 0
sp2 = 0
heart = [60]
avgspo2 = [98]
checkhr = False
checksp = False
#子執行緒的血氧函數
def SPO2():

    while True:
        red, ir = m.read_sequential()
        
        hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

        print("hr detected:",hrb)
        print("sp detected:",spb)
        
        if(hrb == True and hr != -999):
            hr2 = int(hr)
            for i in range(1):
                lastheart = heart.pop()
                if (hr2-lastheart) >= 15:
                    checkhr = True
                    print('Heart Rate too high ->',lastheart)
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
  
#建立子執行緒
t = threading.Thread(target = SPO2)
#執行
t.start()
#**************** GUI part ********************
window = Tk()
window.title("Welcome to People Movement Behavior Demo")
v6String = StringVar()
v6String.set("v6:")
v7String = StringVar()
v7String.set("v7:")
v8String = StringVar()
v8String.set("v8:")
countString = StringVar()
countString.set("0")

hl = Label(window, textvariable= v6String , font=("Arial Bold", 50) ).grid(sticky="W",column = 0 ,row = 0)
bl = Label(window, textvariable= v7String ,font=("Arial Bold", 50)).grid(sticky="W",column=0, row=1)
cl = Label(window, textvariable= v8String ,font=("Arial Bold", 50)).grid(sticky="W",column=0, row=2)
ll = Label(window, textvariable= countString ,font=("Arial Bold", 20)).grid(sticky="W",column=0, row=3)

class globalV:
    count = 0
    lostCount = 0
    startFrame = 0
    frame = 0
    rangeValue = 0.0
    ct = datetime.datetime.now()
    gt = datetime.datetime.now()
    def __init__(self, count):
        self.count = count
        
class v7S:
    tid = 0
    posX = 0.0
    posY = 0.0
    velX = 0.0
    velY = 0.0
    accX = 0.0
    accY = 0.0
    EC = [0.0,0.0,0.0,0.0]
    G = 0.0
        
v7A = [v7S]
        
#UART initial
try:    #pi 3
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
    port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)


gv = globalV(0)

#*****************GPIO Setting*****************************
def my_callback(channel):
    ct = datetime.datetime.now()
    print("intr:{}".format(ct - gv.ct))
    uartIntr("TEST")
    gv.count = gv.count + 1

#****** GPIO 18 for rising edge to catch data from UART ****
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.add_event_detect(18, GPIO.RISING,my_callback)


#
#Object initail
#

pm = peopleMB.PeopleMB(port)

def v7UnpackXY(v7Data):
    print("---v7 unpack---")
    v7xy = []
    for k in v7Data:
        v7xy.append([k[1], k[2]])
    return v7xy

def v7UnpackVelocityXY(v7Data): # velocity x,y
    velxy = []
    for k in v7Data:
        velxy.append([k[3], k[4]])
    return velxy


def uartIntr(name):
    pt = datetime.datetime.now()
    #mmWave/People Movement Behavior tlvRead  
    print(datetime.datetime.now().time())
    #dck=check data
    (dck , v6,v7,v8) = pm.tlvRead(True)
    
    hdr = pm.getHeader()
    #time
    gv.gt = pt
    ct = datetime.datetime.now()
    '''
    print('data')
    print(pt,dck,v6,v7,v8,hdr,ct)
    print(pm)
    print(pm.tlvRead(True))'''
    
    if dck:
        gv.count = 0 
        diff = ct-pt
        f = open('XYtext.txt', 'a')
        print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})] {}".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8),diff))
        xy = v7UnpackXY(v7)
        timeR = str(ct-gv.ct)
        print(xy, file = f) #將xy座標傳送到txt檔
        #print(timeR,file = f) #將時間戳記傳送到txt檔
        print("Position[x,y]:",xy,type(xy))
        vxy = v7UnpackVelocityXY(v7)
        print("Velocity[X,Y]:",vxy,type(xy))
        
        v6String.set("V6 points:{:d}".format(len(v6)))
        v7String.set("V7 Objects:{:d}".format(len(v7)))
        v8String.set("V8 Indexs:{:d}".format(len(v8)))
        countString.set("#{:d} ex:{}".format(hdr.frameNumber, diff))
        pt = ct 
        f.close()
        
        
port.flushInput()
window.mainloop()
GPIO.cleanup()
t.join()
print('done')


