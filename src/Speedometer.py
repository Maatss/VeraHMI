#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, sys, time, math

class Speedometer(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

		self.sensorPin = 40
		self.diameterOfWheel = 0.5 # [m]
		self.wheelCircumference = math.pi*self.diameterOfWheel

		self.speed = 0
		self.lastTIme = time.time()
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
			passedTime = self.newTime - self.lastTIme
			speed = self.wheelCircumference / passedTime

	def speed(self):
		return self.speed
					


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		speed = Speedometer()
		speed.start()
		while True:
			print(speed.speed)
	except (KeyboardInterrupt, SystemExit):
		speed._Thread__stop()
		sys.exit()
