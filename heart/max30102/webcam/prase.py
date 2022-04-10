from RPi import GPIO 
import time

GPIO.setmode(GPIO.BOARD)
buttonPin = 16
GPIO.setup(buttonPin,GPIO.IN)
prev_input = 1
while True:
    input = GPIO.input(buttonPin)
    
    if((not prev_input)and input):
        print("press")
        
        
    prev_input = input
    time.sleep(0.05)