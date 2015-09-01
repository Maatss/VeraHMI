#!/usr/bin/env python

import RPi.GPIO as GPIO
from MySQLConnection import MySQLConnection
import threading, sys, time, math

class Speedometer(threading.Thread):

	def __init__(self, gui, liveData=None, mysql=None, threadLock=None):
		threading.Thread.__init__(self)
		self.daemon = True
		self.mysql = mysql
		self.threadLock = threadLock
		
		self.gui = gui
		self.liveData = liveData

		self.sensorPin = 31
		diameterOfWheel = 0.4816 # [m]
		numersOfMagnets = 4
		self.wheelCircumference = math.pi*diameterOfWheel
		self.distancePerMagnet = self.wheelCircumference / numersOfMagnets

		self.speed = 0
		self.lastTime = time.time()
		self.newTime = time.time()
		self.mysqlTimeSinceLastSave = 0

		self.values = [0, 0, 0]
		self.i = 0

		#Setup GPIO in order to enable button presses
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		#Attach interupts to detect rising edge
		GPIO.add_event_detect(self.sensorPin, GPIO.RISING, callback=self.buttonEvent, bouncetime=10) 

#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		while True:
			if time.time() - self.lastTime > 2:
				self.speed = 0
				for x in range(len(self.values)):
					self.values[x] = 0
				if self.gui: 
					self.gui.setSpeed(self.speed)
				self.liveData.sendSpeed(self.speed)
				self.threadLock.acquire()
				self.mysql.saveSpeed(self.speed)
				self.threadLock.release()
			time.sleep(1)


		
	def buttonEvent(self, channel):
		if GPIO.input(self.sensorPin):
			self.newTime = time.time()
			passedTime = self.newTime - self.lastTime
			
			metersPerSecond = self.distancePerMagnet / passedTime # [m/s]
			if passedTime < 2:
				self.speed = metersPerSecond * 3.6 # [km/h]
			else:
				self.speed = 0

			if self.speed - (sum(self.values) / len(self.values)) > 10:
				self.values[self.i] = self.speed
				self.speed = sum(self.values) / len(self.values)
				self.i += 1
				if self.i > len(self.values)-1:
					self.i = 0

			
			self.mysqlTimeSinceLastSave += passedTime
			if self.mysqlTimeSinceLastSave > 0.2:
				#print(speed)
				if self.gui:
					self.gui.setSpeed(self.speed)

				self.threadLock.acquire()
				self.mysql.saveSpeed(self.speed)
				self.threadLock.release()
				self.mysqlTimeSinceLastSave = 0
				self.liveData.sendSpeed(self.speed)
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
