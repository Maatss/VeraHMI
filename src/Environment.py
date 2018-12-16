#!/usr/bin/env python

import threading, time, sys

if sys.platform == "linux2":
	from src.LiveData import LiveData
	from src.DatabaseHandler import DatabaseHandler



class Environment(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon 	= True
		# set following variable true if debug mode is wanted
		self.debugging 	= False

		self.reset 		= True

		if sys.platform == "linux2":
			self.mysql 		= DatabaseHandler(self)
			self.mysql.start()
		else:
			self.mysql = None

		self.connectedToTeam = False
		
		#### SpeedHandler variables ####
		self.speed 				= 0
		self.meanSpeed 			= 0
		self.totalSpeed			= 0
		self.numerOfSpeedValues = 0

		#### GPSHandler variables ####
		self.gpsPos 			= (None, None)
		self.gpsSpeed 			= 0
		self.gpsConnected		= False

		#### StopWatchHandler variables ####
		self.timerRunning		= False
		self.totalTime 			= (0, 0) # (minutes, seconds)
		self.currentLapTime 	= (0, 0) # (minutes, seconds)
		self.currentLapNumber	= 1
		self.totalTimeStartTime = time.time()
		self.lapTimeStartTime	= time.time()
		self.totalTimeString	= "00:00"
		self.lapTimeString 		= "00:00"


		#### ButtonHandler variables ####


		#### ECUHandler variables ####
		self.cylinderTemp 		= None
		self.topplockTemp 		= None
		self.motorblockTemp 	= None
		self.battyVoltage		= None
		self.airPressure		= None
		self.airTemperture		= None
		self.rpm				= None
		self.fuelMass			= None
		self.ecuErrorCode		= None
		self.ecuConnected 		= False
		self.gpsConnected		= False
		self.ecuDataArray		= [None, None, None, None, None, None, None, None, None]

		


	'''
	##################################################################################################################################################
	####################################################### Internal functions ##########################################################################
	##################################################################################################################################################
	'''

	def timeToString(self, time):
		minutes = time[0]
		seconds = time[1]

		if minutes >= 10:
			string = str(minutes)
		else:
			string = "0" + str(minutes)

		string += ":"

		if seconds >= 10:
			string += str(seconds)
		else:
			string += "0" + str(seconds)
		return string
		


	'''
	##################################################################################################################################################
	####################################################### Class functions ##########################################################################
	##################################################################################################################################################
	'''

	def run(self):
		while True:
			time.sleep(1)
			self.stopWatchEvent()

	#### SpeedHandlerFunction
	def setSpeed(self,speed):
		self.speed 					 = float(speed)
		self.totalSpeed 			+= self.speed
		self.numerOfSpeedValues     += 1
		self.meanSpeed 				 = self.totalSpeed/self.numerOfSpeedValues

		# Save speed in MySQL
		if self.mysql != None and self.timerRunning:
			self.mysql.saveSpeed(self.speed, self.gpsPos)



	#### GPSHandler function
	def setGPSHandlerVariables(self, gpsPos, gpsSpeed, connected):
		self.gpsPos 		= gpsPos
		self.gpsSpeed 		= gpsSpeed
		self.gpsConnected 	= connected


	#### StopWatchHandler function
	def stopWatchEvent(self):
		if self.timerRunning:
			totalSeconds = int(time.time()-self.totalTimeStartTime)
			totalMinutes = int(totalSeconds/60)
			totalSeconds = int(totalSeconds%60)
			#totalMinutes = self.totalTime[0]
			#totalSeconds = self.totalTime[1]
			# Incremet seconds variable and if seconds > 60 incremet minutes and set seconds to zero
			totalSeconds += 1
			if totalSeconds>=60:
				totalSeconds  = 0
				totalMinutes += 1
			self.totalTime = (totalMinutes, totalSeconds)

			# Incremet seconds variable and if seconds > 60 incremet minutes and set seconds to zero
			# Only incremets timer 
			lapSeconds = int(time.time()-self.lapTimeStartTime)
			lapMinutes = int(lapSeconds/60)
			lapSeconds = int(lapSeconds%60)

			lapSeconds += 1
			if lapSeconds>=60:
				lapSeconds  = 0
				lapMinutes += 1
			self.currentLapTime = (lapMinutes, lapSeconds)
			self.totalTimeString = self.timeToString(self.totalTime)
			self.lapTimeString 	= self.timeToString(self.currentLapTime)
			

	def newLapEvent(self):
		self.currentLapNumber 	+= 1
		self.currentLapTime 	 = (0, 0)
		self.lapTimeStartTime	 = time.time()
		self.lapTimeString 		 = self.timeToString(self.currentLapTime)

	#### ButtonHandler functions
	def buttonEvent1(self):
		if self.timerRunning:
			self.newLapEvent()
		else:
			self.resetSpeedVariables()
			self.reset = True
		if self.debugging:
			print("New lap/Reset button pressed")

	def buttonEvent2(self):
		if self.timerRunning:
			self.timerRunning = False
		else:
			self.timerRunning = True

			# Reset mean speed variables 
			self.meanSpeed 			= 0
			self.totalSpeed			= 0
			self.numerOfSpeedValues = 0
			self.totalTimeStartTime = time.time() - self.totalTime[0]*60 		- self.totalTime[1]
			self.lapTimeStartTime	= time.time() - self.currentLapTime[0]*60 	- self.currentLapTime[1]

			if self.reset:
				if self.debugging:
					print("entering reset if-statement..")
				# initiate new tables in database
				if self.mysql != None:
					thread.start_new_thread(self.mysql.createNewSession, ())
				self.reset = False
				self.totalTimeStartTime = time.time()
				self.lapTimeStartTime	= time.time()
				if self.debugging:
					print("Done with initialization of DB")

			self.totalTimeString = self.timeToString(self.totalTime)
			self.lapTimeString 	= self.timeToString(self.currentLapTime)

		if self.debugging:
			print("Start/Stop timer button pressed")


	#### ECUHandler function
	def sendEcuVariables(self, values, connected):
		self.cylinderTemp 		= values[0]
		self.topplockTemp 		= values[1]
		self.motorblockTemp 	= values[2]
		self.battyVoltage		= values[3]
		self.airPressure		= values[4]
		self.airTemperture		= values[5]
		self.rpm				= values[6]
		self.fuelMass			= values[7]
		self.ecuErrorCode		= values[8]
		self.ecuDataArray		= values
		#print(values)
		self.ecuConnected = connected

		# Save values in database
		if self.mysql 	!= None and self.timerRunning:
			self.mysql.saveECUValues(values + [self.gpsPos[0]] + [self.gpsPos[1]] + [self.speed])


	'''
	##################################################################################################################################################
	####################################################### Reset functions ##########################################################################
	##################################################################################################################################################
	'''	

	def resetSpeedVariables(self):
		self.meanSpeed 			= 0
		self.totalSpeed			= 0
		self.numerOfSpeedValues = 0
		self.currentLapNumber	= 1
		self.totalTime 			= (0, 0) # (minutes, seconds)
		self.currentLapTime 	= (0, 0) # (minutes, seconds)
		self.totalTimeStartTime = time.time()
		self.lapTimeStartTime	= time.time()
		self.totalTimeString = self.timeToString(self.totalTime)
		self.lapTimeString 	= self.timeToString(self.currentLapTime)






