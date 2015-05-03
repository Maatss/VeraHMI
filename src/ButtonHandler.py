#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, sys, time

class ButtonHandler(threading.Thread):

	def __init__(self, gui=None, mysql=None):
		threading.Thread.__init__(self)
		self.gui = gui
		self.mysql = mysql

		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(38, GPIO.RISING, callback=self.buttonEvent, bouncetime=300) 
		GPIO.add_event_detect(40, GPIO.RISING, callback=self.buttonEvent, bouncetime=300)
	
	def run(self):
		time.sleep(1)
		
	def buttonEvent(self, channel):
		if channel == 38:
			if self.gui != None:
				if self.gui.timerIsRunning():
					self.gui.newLap()
					print("New lap pressed")
				else:
					self.gui.reset()
					print("Reset pressed")
			else:
				print("New lap/Reset button pressed")

		if channel == 40:
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
