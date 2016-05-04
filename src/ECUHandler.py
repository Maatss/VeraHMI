#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, time, sys, os.path
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
		#self.portName 			= "/dev/ttyACM0"
		self.portName 			= "/dev/serial/by-id/usb-FTDI_UM232R_USB__-__Serial_FTCAN7QC-if00-port0"

		try:
			self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			self.port.flushInput()
		except Exception as e:
			#print(e)
			print("Could not connect to ECU, continuing...")



#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def parseData(self,dataString):
		mode, data = dataString.split(':')
		mode = mode.split('#')[1]
		data=data.split('+')
		data[-1] = data[-1].split('&')[0]
		return (mode,data)


	def findNextLog(self):
		self.logs = [None, None, None, None, None, None, None, None, None]
		mode	  =  ""
		try:
			dataString = self.port.readline()
			if len(dataString)>0:
				mode,self.logs = self.parseData(dataString)
		except Exception as e:
			#print(e)
			pass

		if(self.logs[1] != None and mode == "BASE"):
			# Set ECU to be connected
			self.connected = True

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
				self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			except Exception as e:
				pass
				#print(e)

		# Send ECU values to Environment
		if self.environment != None:
			self.environment.sendEcuVariables(self.logs, self.connected)
		return True


	def checkForError(self, error_code):
		error_code = uint32(error_code)
		#print(error_code)
		'''
		TODO: Implement this...
		'''

	def run(self):
		while True:
			self.findNextLog()
					


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



