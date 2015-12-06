#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, sys, time

class ButtonHandler(threading.Thread):

	def __init__(self, environment=None):
		threading.Thread.__init__(self)
		self.daemon = True
		self.environment = environment

		self.startStopBtn = 11
		self.lapResetBtn = 12 

		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.startStopBtn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.lapResetBtn,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		#Attach interupts to detect rising edge
		GPIO.add_event_detect(self.startStopBtn, GPIO.RISING, callback=self.buttonEvent, bouncetime=200) 
		GPIO.add_event_detect(self.lapResetBtn,  GPIO.RISING, callback=self.buttonEvent, bouncetime=200)
	

#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		pass
		
	def buttonEvent(self, channel):
		if channel == self.lapResetBtn:
			#if GPIO.input(self.lapResetBtn):
			self.environment.buttonEvent1()
			if __name__ == '__main__':
				print("button 1 pressed")


		elif channel == self.startStopBtn:
			self.environment.buttonEvent2()				
			if __name__ == '__main__':
				print("button 2 pressed")		


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		btn = ButtonHandler()
		btn.start()
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		btn._Thread__stop()
		sys.exit()
