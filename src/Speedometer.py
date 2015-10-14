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

		#System parameters
		self.sensorPin = 31
		diameterOfWheel = 0.4816 # [m]
		numersOfMagnets = 4
		self.wheelCircumference = math.pi*diameterOfWheel
		self.distancePerMagnet = self.wheelCircumference / numersOfMagnets
		self.refreshTimeGUI = 0.2 # [every X seconds]

		#Initial values
		self.speed = 0
		self.lastTime = time.time()
		self.newTime = time.time()
		self.mysqlTimeSinceLastSave = 0
		self.timeSinceGUIUpdate = 0

		#Running mean vector (the size of the vector can be changed to the desired number of entries)
		self.values = [0, 0, 0]
		self.GUISpeed = []
		self.i = 0

		#Setup GPIO for the sensor
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		#Attach interupts to detect rising edge
		GPIO.add_event_detect(self.sensorPin, GPIO.RISING, callback=self.sensorEvent, bouncetime=50) 

#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		while True:
			if time.time() - self.lastTime > 1:
				self.speed = 0
				for x in range(len(self.values)):
					self.values[x] = 0
				self.GUISpeed = []
				self.timeSinceGUIUpdate += time.time() - self.lastTime
				if self.gui: 
					self.gui.setSpeed(self.speed)
				self.liveData.sendSpeed(self.speed)
				self.threadLock.acquire()
				self.mysql.saveSpeed(self.speed)
				self.threadLock.release()
			time.sleep(1)


		
	def sensorEvent(self, channel):
		if GPIO.input(self.sensorPin):
			self.newTime = time.time()
			passedTime = self.newTime - self.lastTime
			
			metersPerSecond = self.distancePerMagnet / passedTime # [m/s]
			if passedTime < 1:
				self.speed = metersPerSecond * 3.6 # [km/h]
			else:
				self.speed = 0

			self.values[self.i] = self.speed
			self.GUISpeed.append(self.speed)
			self.speed = sum(self.values) / len(self.values)
			self.i += 1
			if self.i > len(self.values)-1:
				self.i = 0

			self.timeSinceGUIUpdate += passedTime
			
			if self.gui and self.timeSinceGUIUpdate > self.refreshTimeGUI:
				#print(speed)
				speedToGUI = sum(self.GUISpeed) / len(self.GUISpeed)
				self.gui.setSpeed(speedToGUI)
				self.liveData.sendSpeed(speedToGUI)
				self.timeSinceGUIUpdate = 0
				self.GUISpeed = []

			self.mysqlTimeSinceLastSave += passedTime
			if self.mysqlTimeSinceLastSave > 0.2:
				self.threadLock.acquire()
				self.mysql.saveSpeed(self.speed)
				self.threadLock.release()
				self.mysqlTimeSinceLastSave = 0
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
