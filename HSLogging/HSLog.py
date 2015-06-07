#!/usr/bin/env python

from LogMySQL import LogMySQL

import serial, threading, time, sys, os.path

class Logger(threading.Thread):

	def __init__(self, commandName, logNames, mysql, debug):
		threading.Thread.__init__(self)
		self.daemon=True
		self.logNames = logNames
		self.commandName = commandName
		self.mysql = mysql
		self.debug = debug

		#Baudrate
		self.BAUDRATE = 230400
		self.portName = self.findPort()
		try:
			self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
			self.port.flushInput()
			print("Connected to ECU, waiting for data.\n")
		except:
			print("Could not connect to ECU, continuing...\n")

		self.logs = [None]*len(self.logNames)


	def findNumberBefore(self, char, data, x):
		numberString = ""
		while True:
			number = data[x]
			x += 1
			if number != char:
				numberString += number 
			else:
				return (x, int(numberString))


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


	def findPort(self):
		if os.path.exists("/dev/ttyUSB0"):
			return "/dev/ttyUSB0"
		elif os.path.exists("/dev/ttyUSB1"):
			return "/dev/ttyUSB1"


	def findNextLog(self):
		data = self.readECU()
		if(data != None):
			x=0
			if data[x]=="\r" or data[x]=="\n":
				x = 2

			if data[x] == "#":
				x += 1
				command = ""
				while data[x] != ":":
					command += data[x]
					x += 1
				print("Command: " + command)
				if command == sef.commandName:
					x += 1
					for i in range(len(self.logNames)):
						(x, self.logs[i]) = self.findNumberBefore("+", data, x)
					# Find last data
					(x, self.logs[len(self.logNames)]) = self.findNumberBefore("&", data, x)
					return True
				else:
					print("Invalid command found: " + command)
		else:
			self.logs = [None]*len(self.logNames)
			if self.debug:
				print("jibberish found: " + str(data))
			try:
				self.portName = self.findPort()
				self.port = serial.Serial(self.portName, baudrate=self.BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
				#print("ECU detected, waiting for data.\n")
			except:
				pass
				
			return False


	def run(self):
		while True:
			if(self.findNextLog()):
				self.mysql.saveLog(self.logs)
				print("Values logged")





#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		logNames = ["RPM", "calc_fuel_mass", "calc_fuel_stop", "calc_charge_time", "cycle_charge_time", 
					"calc_ign_pos", "calc_inl_port_open_pos", "calc_inl_port_closing_pos", "calc_exh_port_open_pos", 
					"calc_exh_port_closing_pos", "cylinder_temperature", "acc_voltage", "air_pressure", 
					"air_temperature", "kam-signal1", "kam-signal2", "injector_hi", "injector_low", "injector_off",
					"ignition_charge", "ignition", "inlet_port_high", "inlet_port_low", "exhaust_port_hi", 
					"exhaust_port_low", "vev_signal", "run_high/low", "clutch_promille", "error_code"]

		MySQLString =  """
							CREATE TABLE IF NOT EXISTS HSLog%s
							(`id` int(11) NOT NULL AUTO_INCREMENT,
							`timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
							`RPM` int(15) NOT NULL,
							`calc_fuel_mass` int(15) NOT NULL,
							`calc_fuel_stop` int(15) NOT NULL,
							`calc_charge_time` int(15) NOT NULL,
							`cycle_charge_time` int(15) NOT NULL,
							`calc_ign_pos` int(15) NOT NULL,
							`calc_inl_port_open_pos` int(15) NOT NULL,
							`calc_inl_port_closing_pos` int(15) NOT NULL,
							`calc_exh_port_open_pos` int(15) NOT NULL,
							`calc_exh_port_closing_pos` int(15) NOT NULL,
							`cylinder_temperature` int(15) NOT NULL,
							`acc_voltage` int(15) NOT NULL,
							`air_pressure` int(15) NOT NULL,
							`air_temperature` int(15) NOT NULL,


							`kam-signal1` int(15) NOT NULL,
							`kam-signal2` int(15) NOT NULL,
							`injector_hi` int(15) NOT NULL,
							`injector_low` int(15) NOT NULL,
							`injector_off` int(15) NOT NULL,
							`ignition_charge` int(15) NOT NULL,
							`ignition` int(15) NOT NULL,
							`inlet_port_high` int(15) NOT NULL,
							`inlet_port_low` int(15) NOT NULL,
							`exhaust_port_hi` int(15) NOT NULL,
							`exhaust_port_low` int(15) NOT NULL,
							`vev_signal` int(15) NOT NULL,
							`run_high/low` int(15) NOT NULL,
							`clutch_promille` int(15) NOT NULL,
							`error_code` int(15) NOT NULL,

							PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci AUTO_INCREMENT=1;
							"""

		dataBase = LogMySQL(logNames, MySQLString)
		dataBase.startLogging()
		log = Logger("CYCLE", logNames, dataBase, False)
		log.start()

		#dont exit main thread before log thread
		while True:
			pass

	except Exception as e:
		print("Error when logging: " + str(e))
		log._Thread__stop()
		print("Exiting...")
		sys.exit()



