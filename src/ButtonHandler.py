#!/usr/bin/env python

import RPi.GPIO as GPIO

class ButtonHandler(threading.Thread):

	def __init__(self, gui = None):
		threading.Thread.__init__(self)
		self.gui = gui
		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	def run(self):
		GPIO.add_event_detect(36, GPIO.RISING, callback=buttonEvent, bouncetime=300) 
		GPIO.add_event_detect(38, GPIO.RISING, callback=buttonEvent, bouncetime=300) 
		GPIO.add_event_detect(40, GPIO.RISING, callback=buttonEvent, bouncetime=300)
		
	def buttonEvent(channel):
	if channel == 38:
		if gui.timerIsRunning():
			gui.newLap()
			print("New lap pressed")
		else:
			gui.reset()
			print("Reset pressed")

	if channel == 40:
		if gui.timerIsRunning():
			gui.stopTimer()
			print("Stop pressed")
		else:
			gui.startTimer()
			print("Start pressed")