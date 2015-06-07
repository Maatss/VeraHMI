#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MySQLConnection import MySQLConnection

import serial, threading, time, sys, os.path
from numpy import uint32


class ECUHandler(threading.Thread):

	def __init__(self, gui = None, gps = None, mysql = None, debug = False, threadLock=None):
		threading.Thread.__init__(self)
		self.daemon=True
		self.connected = False
		self.threadLock = threadLock

		#Baudrate
		self.BAUDRATE = 230400
		#This if statement is only here to make it work when modul is run as main thread
		if mysql != None:
			self.mysql = mysql
		else:
			self.mysql = MySQLConnection()

		self.gui, self.gps, self.debug = gui, gps, debug

		self.unavailableCount = 0
		self.logNames= ["cylinder temp", "topplock temp", "motorblock temp", "batterispänning", "lufttryck", "lufttemperatur", "varvtal", "bränslemassa", "error code"]
		if self.gui != None:
			self.gui.setStatus(1, 2, "Started")
		self.portName = self.findPort()
		#print("Port name: " + self.portName)

		try:
			self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			self.port.flushInput()
		except:
			print("Could not connect to ECU, continuing...")


#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def findPort(self):
		# Set the device name depending on the OS ("darwin" = OS X, "linux2" = raspbian)
		if sys.platform == "darwin":
			return "/dev/tty.usbserial-A96T5FJN"
		else:
			if os.path.exists("/dev/ttyUSB0"):
				return "/dev/ttyUSB0"
			elif os.path.exists("/dev/ttyUSB1"):
				return "/dev/ttyUSB1"

	def readECU(self):
	    rv = ""
	    while True:
	    	try:
	        	ch = self.port.read()
	        except:
	        	return None
		rv += ch
	        if ch=='&':
	        	return rv


	def findNumberBefore(self, char, data, x):
		numberString = ""
		while True:
			number = data[x]
			x += 1
			if number != char:
				numberString += number 
			else:
				return (x, int(numberString))

	def findNextLog(self):
		self.logs = [-1, -1, -1, -1, -1, -1, "----", -1, -1]
		data = self.readECU()
		if(data != None):
			x=2
			# Set ECU to be connected
			self.connected = True
			self.gui.connectECUNoLog()
			if self.gui and self.unavailableCount>=5:
				self.gui.connectECU()
				print("ECU connected")
			self.unavailableCount = 0

			if data[x] == "#":
				x += 1
				command = ""
				while data[x] != ":":
					command += data[x]
					x += 1
				#print("Command: " + command)
				if command == "BASE":
					x += 1
					for i in range(0, 8):
						(x, self.logs[i]) = self.findNumberBefore("+", data, x)
					# Find last data
					(x, self.logs[8]) = self.findNumberBefore("&", data, x)

					return self.logs

			else:
				if self.debug:
					print("jibberish found: " + str(data))
		else:
			if self.debug:
				print("Serial not available")
			time.sleep(1)
			self.unavailableCount += 1
			#print("unavailableCount: " + str(self.unavailableCount) + "Connected: " + str(self.connected))
			if self.unavailableCount >= 5:
				if self.gui and self.connected:
					self.gui.disconnectECU()
					print("ECU disconnected")
				elif self.gui:
					self.gui.disconnectECUNoLog()
				
				self.connected = False
				try:
					self.port.close()
				except:
					pass
			try:
				self.portName = self.findPort()
				self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			except:
				pass


	def getGPSPos(self):
		if sys.platform == "linux2" and self.gps != None:
			(lat, lon, speed) = self.gps.getGPSPos()
			if speed:
				speed = speed # want speed in Km/h not m/s
			#print("lat: " + str(lat) + " Lon: " + str(lon) + " Alt: " + str(alt) + " Speed: " + str(speed))
			return [lat, lon, speed]
		else:
			return [None, None, None]
		
	def updateGUI(self):
		self.gui.setRPM(self.logs[6])
		self.gui.setTemp(self.logs[1], self.logs[2], self.logs[0])


	def checkForError(self, error_code):
		error_code = uint32(error_code)
		#print(error_code)
		'''
		TODO: Implement this...
		'''

	def run(self):

		while True:
			if(self.findNextLog()):
				gpsData = self.getGPSPos()
				#Handle error codes
				self.checkForError(self.logs[8])

				#Save logs in MySQL
				self.threadLock.acquire()
				self.mysql.saveLog(self.logs + gpsData)
				self.threadLock.release()

				#Update GUI data
				if self.gui:
					if gpsData[2]:
						self.gui.setSpeed(gpsData[2])
					self.updateGUI()

				#Print data if in debug mode
				if self.debug:
					print(self.logs + gpsData)
				
					


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		if sys.platform == "linux2":
			from GPSHandler import GPSHandler
			GPSHandler = GPSHandler()
			GPSHandler.start()
			ecu = ECUHandler(gps = GPSHandler, debug=True)
		else:
			ecu = ECUHandler(debug=True)
		ecu.start()
		while True:
			time.sleep(1)
			
	except (KeyboardInterrupt, SystemExit):
		if sys.platform == "linux2":
			GPSHandler._Thread__stop()
		ecu._Thread__stop()
		sys.exit()



