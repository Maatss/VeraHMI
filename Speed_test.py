#!/usr/bin/env python

import RPi.GPIO as GPIO
import time


#Setup GPIO in order to enable button presses
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def buttonEvent(event):
	print("OK")

#Attach interupts to detect rising edge
GPIO.add_event_detect(31, GPIO.BOTH, callback=buttonEvent, bouncetime=100) 


while True:
	time.sleep(0.5)