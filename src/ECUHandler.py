#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, time, sys, os.path
if sys.platform == "linux2":
	import serial
	from numpy import uint32


class ECUHandler(threading.Thread):

	def __init__(self, environment=None):
		threading.Thread.__init__(self)
		self.daemon				= True
		self.environment		= environment
		
		# Parameters
		self.BAUDRATE 			= 230400
		self.connected 			= False
		self.logNames			= ["cylinder temp", "topplock temp", "motorblock temp", "batterispänning", "lufttryck", "lufttemperatur", "varvtal", "bränslemassa", "error code"]
		self.portName 			= self.findPort()

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
	        except Exception as e:
				#print(e)
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
		self.logs = [None, None, None, None, None, None, None, None, None]
		data = self.readECU()
		if(data != None):
			x=2
			# Set ECU to be connected
			self.connected = True

			if data[x] == "#":
				x 		+= 1
				command  = ""
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

			else:
				print("jibberish found: " + str(data))
		else:
			#print("Serial not available")
			time.sleep(1)
			self.connected = False
			try:
				self.port.close()
			except Exception as e:
				pass
				#print(e)
			try:
				self.portName 	= self.findPort()
				self.port 		= serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			except Exception as e:
				pass
				#print(e)

		# Send ECU values to Environment
		self.environment.sendEcuVariables(self.logs, self.connected)


	def checkForError(self, error_code):
		error_code = uint32(error_code)
		#print(error_code)
		'''
		TODO: Implement this...
		'''

	def run(self):
		while True:
			if(self.findNextLog()):
				self.checkForError(self.logs[8])
					


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		ecu = ECUHandler()
		ecu.start()

		while True:
			time.sleep(1)
			
	except (KeyboardInterrupt, SystemExit):
		ecu._Thread__stop()
		sys.exit()



