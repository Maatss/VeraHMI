import RPi.GPIO as GPIO
import serial
import sys
import time

def readECU(port):
    rv = ""
    while True:
        ch = port.read()
	rv += ch
        if ch=='&':
            return rv


GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, True)
#time.sleep(0.5)

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
port.write("OP:"+sys.argv[1]+"_ID:"+sys.argv[2]+"_VAL:"+sys.argv[3]+"&\r\n")

rvc = port.readline()
print rvc

GPIO.output(13, False)
GPIO.cleanup()
