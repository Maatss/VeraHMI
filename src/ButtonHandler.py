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
		GPIO.add_event_detect(self.startStopBtn, GPIO.RISING, callback=self.buttonEvent, bouncetime=1000) 
		GPIO.add_event_detect(self.lapResetBtn, GPIO.RISING, callback=self.buttonEvent, bouncetime=1000)
	
	def run(self):
		time.sleep(1)
		
	def buttonEvent(self, channel):
		if channel == self.startStopBtn:
			if self.gui != None:
				if self.gui.timerIsRunning():
					self.gui.newLap()
					print("New lap pressed")
				else:
					self.gui.reset()
					print("Reset pressed")
			else:
				print("New lap/Reset button pressed")

		if channel == self.lapResetBtn:
			if self.gui != None:
				if self.gui.timerIsRunning():
					self.gui.stopTimer()
					self.mysql.stopLogging()
					self.gui.saveHMILog(1, 2, "Stopped logging")
					print("Stop pressed")
				else:
					self.gui.startTimer()
					self.mysql.startLogging()
					self.gui.saveHMILog(1, 2, "Started logging")
					print("Start pressed")
			else:
				print("Start/Stop timer button pressed")
				
			
				


if __name__ == '__main__':
	try:
		btn = ButtonHandler()
		btn.start()
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		btn._Thread__stop()
		sys.exit()
