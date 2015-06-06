#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, sys, time, math

class Speedometer(threading.Thread):

	def __init__(self, gui):
		threading.Thread.__init__(self)
		self.daemon = True
		
		self.gui = gui

		self.sensorPin = 31
		diameterOfWheel = 0.5 # [m]
		numersOfMagnets = 1
		self.wheelCircumference = math.pi*diameterOfWheel
		self.distancePerMagnet = self.wheelCircumference / numersOfMagnets

		self.speed = 0
		self.lastTime = time.time()
		self.newTime = time.time()

		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		#Attach interupts to detect rising edge
		GPIO.add_event_detect(self.sensorPin, GPIO.RISING, callback=self.buttonEvent, bouncetime=100) 

#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		time.sleep(1)
		
	def buttonEvent(self, channel):
		if GPIO.input(self.sensorPin):
			self.newTime = time.time()
			passedTime = self.newTime - self.lastTime
			metersPerSecond = self.wheelCircumference / passedTime # [m/s]
			speed = metersPerSecond * 3.6 # [km/h]
			#print(speed)
			if self.gui:
				self.gui.setSpeed(speed)
			self.lastTime = self.newTime

	def getSpeed(self):
		return self.speed
					


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		speed = Speedometer(None)
		speed.start()
		while True:
			time.sleep(0.5)
	except (KeyboardInterrupt, SystemExit):
		speed._Thread__stop()
		sys.exit()
