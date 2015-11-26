#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, time, math, sys

class SpeedHandler(threading.Thread):

	def __init__(self, environment=None):
		threading.Thread.__init__(self)

		# Make thread kill it self when parent dies
		self.daemon 				= True

		# Set environment instance
		self.environment 			= environment

		# System parameters
		self.sensorPin 				= 13
		diameterOfWheel 			= 0.4816 # [m]
		numersOfMagnets 			= 4
		self.wheelCircumference 	= math.pi*diameterOfWheel
		self.distancePerMagnet 		= self.wheelCircumference/numersOfMagnets
		self.timeIntervall 			= 0.2									# send value every X seconds
		self.eventHappened			= False									
		self.timeUntilZero			= 0.8									# If it has been more than X seconds since last sensor event, set speed to zero

		# Initial values
		self.lastTime 				= time.time()
		self.newTime 				= time.time()
		self.speed 					= []
		self.speedToSend			= 0

		# Setup GPIO for the sensor
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Attach interupts to detect rising edge
		GPIO.add_event_detect(self.sensorPin, GPIO.RISING, callback=self.sensorEvent, bouncetime=50) 


#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		while True:
			self.sendSpeed()
			time.sleep(self.timeIntervall)

		
	def sendSpeed(self):
		if len(self.speed) != 0 and self.eventHappened:
			self.speedToSend = sum(self.speed) / len(self.speed)
		else:
			if time.time() - self.lastTime > self.timeUntilZero:
				self.speedToSend = 0

		if self.environment != None:
			self.environment.setSpeed(self.speedToSend)
		else:
			print("Speed: " + str(self.speedToSend))

		self.speed = []
		self.eventHappened = False


	def sensorEvent(self, channel):
		if GPIO.input(self.sensorPin):
			self.newTime 	= time.time()
			passedTime 		= self.newTime - self.lastTime

			# Calulate speed and add it to the speed array
			metersPerSecond = self.distancePerMagnet / passedTime # [m/s]
			self.speed.append(metersPerSecond * 3.6)# [km/h]

			self.eventHappened = True
			self.lastTime = self.newTime



#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		speed = SpeedHandler()
		speed.start()
		while True:
			time.sleep(0.5)
	except (KeyboardInterrupt, SystemExit):
		speed._Thread__stop()
		sys.exit()
