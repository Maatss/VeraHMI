#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, threading, time, sys, os.path
from MySQLConnection import MySQLConnection

class ECUHandler(threading.Thread):

	def __init__(self, gui = None, gps = None, mysql = None, debug = False):
		threading.Thread.__init__(self)
		self.daemon=True
		if mysql != None:
			self.mysql = mysql
		else:
			self.mysql = MySQLConnection()
		self.gui = gui
		self.gps = gps
		self.debug = debug

		self.unavailableCount = 0
		self.logNames= ["cylinder temp", "topplock temp", "motorblock temp", "batterispänning", "lufttryck", "lufttemperatur", "varvtal", "bränslemassa", "error code"]
		if self.gui != None:
			self.gui.setStatus(1, 2, "Started")
		self.portName = self.findUSB()
		#print("Port name: " + self.portName)

		try:
			self.port = serial.Serial(self.portName, baudrate=115200, timeout=3.0)
			self.port.flushInput()
		except:
			print("Could not connect to ECU, continuing...")

	def findUSB(self):
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
	        	self.connected = False
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
			y=0
			x=0
			# Set ECU to be connected
			if self.gui:
				self.gui.connectECU()
			self.unavailableCount = 0

			if data[x] == "#":
				x += 1
				command = ""
				while data[x] != ":":
					command += data[x]
					x += 1
				if command == "BASE":
					x += 1
					for i in range(0, 8):
						(x, self.logs[i]) = self.findNumberBefore("+", data, x)
					# Find last data
					(x, self.logs[8]) = self.findNumberBefore("&", data, x)
					'''
					print("Logs found!\n")
					
					for i in range(0,9):
						printStr = self.logNames[i] + ": " + str(self.logs[i])
						print(printStr)
					print("\n")
					'''
					return self.logs

			else:
				print("jibberish found... :( \n")
		else:
			print("Serial not available")
			time.sleep(1)
			self.unavailableCount += 1
			if self.unavailableCount == 5:
				print("ECU disconnected")
				if self.gui:
					self.gui.disconnectECU()
				self.connected = False
				try:
					self.port.close()
				except:
					pass
			try:
				self.portName = self.findUSB()
				self.port = serial.Serial(self.portName, baudrate=115200, timeout=3.0)
			except:
				pass


	def getGPSPos(self):
		if sys.platform == "linux2" and self.gps != None:
			(lat, lon, alt, speed) = self.gps.getGPSPos()
			#print("lat: " + str(lat) + "Lon: " + str(lon) + "Alt: " + str(alt) + "Speed: " + str(speed))
			return [lat, lon, alt, speed]
		else:
			return [None, None, None, None]
		
	def updateGUI(self):
		self.gui.setRPM(self.logs[6])

	def run(self):

		while True:
			if(self.findNextLog()):
				gpsData = self.getGPSPos()
				self.mysql.saveLog(self.logs + gpsData[0:2])
				if self.gui:
					if gpsData[3]:
						self.gui.setSpeed(gpsData[3])
					self.updateGUI()

				if self.debug:
					print(self.logs + gpsData)
				
					

if __name__ == '__main__':
	try:
		ecu = ECUHandler(debug=True)
		ecu.start()
		while True:
			time.sleep(1)
			
	except (KeyboardInterrupt, SystemExit):
		ecu._Thread__stop()
		sys.exit()



