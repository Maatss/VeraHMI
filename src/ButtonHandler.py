#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, sys, time

class ButtonHandler(threading.Thread):

	def __init__(self, gui=None, mysql=None):
		threading.Thread.__init__(self)
		self.gui = gui
		self.mysql = mysql
		self.startStopBtn = 38
		self.lapResetBtn = 40

		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.startStopBtn, GPIO.IN)
		GPIO.setup(self.lapResetBtn, GPIO.IN)

		#Attach interupts to detect rising edge
		GPIO.add_event_detect(self.startStopBtn, GPIO.RISING, callback=self.buttonEvent, bouncetime=1000) 
		GPIO.add_event_detect(self.lapResetBtn, GPIO.RISING, callback=self.buttonEvent, bouncetime=1000)
	

#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		time.sleep(1)
		
	def buttonEvent(self, channel):
		if channel == self.startStopBtn:
			if self.gui != None:
				if self.gui.timerIsRunning():
					print("New lap pressed")
					self.gui.newLap()
				else:
					print("Reset pressed")
					self.gui.reset()	
			else:
				print("New lap/Reset button pressed")

		if channel == self.lapResetBtn:
			if self.gui != None:
				if self.gui.timerIsRunning():
					print("Stop pressed")
					self.gui.stopTimer()
					self.mysql.stopLogging()
					self.gui.saveHMILog(1, 2, "Stopped logging")
				else:
					print("Start pressed")
					self.gui.startTimer()
					self.mysql.startLogging()
					self.gui.saveHMILog(1, 2, "Started logging")
			else:
				print("Start/Stop timer button pressed")
							


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
