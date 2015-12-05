#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading, time, math, sys

class SpeedHandler(threading.Thread):

	def __init__(self, environment=None):
		threading.Thread.__init__(self)

		# Make thread kill itself when parent dies
		self.daemon 				= True

		# Set environment instance
		self.environment 			= environment

		# System parameters
		self.sensorPin 				= 13
		diameterOfWheel 			= 0.4816 # [m]
		numersOfMagnets 			= 4
		self.wheelCircumference 	= math.pi*diameterOfWheel
		self.distancePerMagnet 		= self.wheelCircumference/numersOfMagnets
		self.timeIntervall 			= 0.5	# send value every X seconds
		self.eventHappened			= False									
		self.timeUntilZero			= 1		# If it has been more than X seconds since last sensor event, set speed to zero

		# Initial values
		self.lastTime 				= time.time()
		self.newTime 				= time.time()
		self.speed 					= []
		self.speedToSend			= 0

		# Setup GPIO for the sensor
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Attach interupts to detect rising edge
		GPIO.add_event_detect(self.sensorPin, GPIO.RISING, callback=self.sensorEvent, bouncetime=20) 


#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		while True:
			self.sendSpeed()
			time.sleep(self.timeIntervall)

		
	def sendSpeed(self):
		if len(self.speed) != 0 and self.eventHappened:
			self.speedToSend = int(round(sum(self.speed) / len(self.speed)))
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
		self.newTime 	= time.time()
		if GPIO.input(self.sensorPin):
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
