#!/usr/bin/env python


#Import GUI module 
from Tkinter import *

#Import our own modules/objects
from timer import TimerFrame
from status_bar import Status_bar
from GPS_ECU_status import GPS_ECU_status
from Speed import Speed
from RPM import RPM
from temp import Temp
from SpeedometerGUI import SpeedometerGUI

#Append parent folder in order to be able to import from src folder
import sys, time
if sys.platform == "linux2":
	sys.path.append('/home/pi/VeraHMI')
	sys.path.append('/Users/andreaskall/VeraHMI')
	from src.MySQLConnection import MySQLConnection


class GUI(Tk):
	def __init__(self, mysql = None):
		Tk.__init__(self)
		self.mysql = mysql
		self.gps = None

		#Variable to keep track wether or not to log data (only log data when timer is running)
		self.logging = True

		#Setup screen
		self.width, self.height = 700, 480
		self.config(bg="black")
		self.bind('<Escape>', self.end_fullscreen)
		self.bind('<space>', self.start_fullscreen)
		#self.minsize(self.width, self.height)
		self.columnconfigure(3, weight=1)
		self.rowconfigure(3, weight=1)
		self.title("Vera HMI")
		self.config(cursor="none")

		#Put GUI in the center of the screen 
		x = (self.winfo_screenwidth() / 2) - (self.width / 2)
		y = (self.winfo_screenheight() / 2) - (self.height / 2)
		self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

		#GPS and ECU Status
		self.GPS_ECU_status = GPS_ECU_status()
		self.GPS_ECU_status.grid(row=0, column=3, sticky=E)
		self.GPS_ECU_status.config(padx=10)

		# Speed
		self.speed = SpeedometerGUI(400, 40, 8)
		self.speed.grid(row=3, column=0, sticky=SW)
		
		#Timer
		self.timer = TimerFrame()
		self.timer.grid(row=3, column=2, columnspan=2, rowspan=2, sticky=SE)
		self.timer.config(padx=20, pady=10)

		# Status
		self.status = Status_bar()
		self.status.config(padx=20)
		self.status.grid(row=0, column=0, columnspan=3, sticky=W)

		# RPM
		self.rpm = RPM()
		self.rpm.grid(row=4, column=0, sticky=SW)
		self.rpm.config(padx=20, pady=10)

		#Temp status
		self.temp = Temp()
		self.temp.grid(row=1, column=0, rowspan=2, sticky=NW)
		self.temp.config(padx=20, pady=20)


#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def stopTimer(self):
		self.timer.stopCount()
		self.setStatus(1, 3, "Stopped")

	def isLogging(self):
		return self.logging

	def timerIsRunning(self):
		return self.timer.isRunning()

	def resetMeanSpeed(self):
		self.speed.reset()


	def reset(self):
		self.timer.reset()
		self.speed.reset()
		self.setStatus(1, 3, "Reset timer")
		self.logging = False

	def newLap(self):
		if self.timerIsRunning:
			(lapTime, lapNr) = self.timer.newLap()
			self.setStatus(1, 3, "New lap")
			if sys.platform == "linux2":
				date = time.strftime("%Y-%m-%d")
				(lat, lon, speed) = self.getGPSPos()
				self.mysql.saveHMILog(date, 1, 3, "Lap #" + str(lapNr) + " time: " + lapTime, [lat, lon])

	def startTimer(self):
		self.timer.startCount()
		self.setStatus(1, 3, "Started")
		if self.logging == False:
			self.logging = True

	def connectGPS(self):
		if not self.GPS_ECU_status.isGPSConnected():
			self.GPS_ECU_status.GPS_connected(True)
			self.saveHMILog(1, 1, "Connected")

	def connectGPSNoLog(self):
		self.GPS_ECU_status.GPS_connected(True)

	def disconnectGPS(self):
		if self.GPS_ECU_status.isGPSConnected():
			self.GPS_ECU_status.GPS_connected(False)
			self.saveHMILog(1, 1, "Disconnected")

	def disconnectGPSNoLog(self):
		self.GPS_ECU_status.GPS_connected(False)
		
	def connectECU(self):
		if not self.GPS_ECU_status.isECUConnected():
			self.GPS_ECU_status.ECU_connected(True)
			self.saveHMILog(1, 2, "Connected")

	def connectECUNoLog(self):
		self.GPS_ECU_status.ECU_connected(True)

	def disconnectECU(self):
		if self.GPS_ECU_status.isGPSConnected():
			self.GPS_ECU_status.ECU_connected(False)
			self.temp.reset()
			self.rpm.reset()
			self.saveHMILog(1, 2, "Disconnected")

	def disconnectECUNoLog(self):
		self.GPS_ECU_status.ECU_connected(False)
		
	def getGPSPos(self):
		if sys.platform == "linux2" and self.gps != None:
			return self.gps.getGPSPos()
		else:
			return (None, None, None)

	def saveHMILog(self, level, module, message):
		if sys.platform == "linux2":
			#modules: 1=GPSHAndler, 2=ECUHandler, 3=StopWatch
			(lat, lon, speed) = self.getGPSPos()
			date = time.strftime("%Y-%m-%d")
			if self.mysql != None:
				self.mysql.saveHMILog(date, level, module, message, [lat, lon])

	def setStatus(self, level, module, message):
		
		self.status.set_status(int(level), int(module), message)
		self.saveHMILog(level, module, message)

	def setSpeed(self, speed):
		self.speed.setSpeed(speed)

	def setRPM(self, rpm):
		self.rpm.setRPM(rpm)

	def end_fullscreen(self, event=None):
	    self.attributes("-fullscreen", False)

	def start_fullscreen(self, event=None):
	    self.attributes("-fullscreen", True)

	def setGPS(self, gps):
		self.gps = gps

	def setTemp(self, tempTopplock, tempMotor, tempCylinder):
		self.temp.setTemp(tempTopplock, tempMotor, tempCylinder)



#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	def checkSerial(GUI):
		var = raw_input("Enter command: " )
		if var == "stop":
			GUI.stopTimer()
		elif var == "lap":
			GUI.newLap()
		elif var == "start":
			GUI.startTimer()
		elif var == "GPS_ON":
			GUI.connectGPS()
		elif var == "GPS_OFF":
			GUI.disconnectGPS()
		elif var == "ECU_ON":
			GUI.connectECU()
		elif var == "ECU_OFF":
			GUI.disconnectECU()
		elif var == "status":
			level = raw_input("Enter level: ")
			module = raw_input("enter module number: ")
			string = raw_input("Enter status: ")
			GUI.setStatus(level, module, string)
		elif var == "q":
			GUI.quit()
		elif var == "speed":
			spd = raw_input("Enter speed: ")
			GUI.setSpeed(spd)
		elif var == "rpm":
			r = raw_input("Enter RPM: ")
			GUI.setRPM(r)
		elif var == "btn1":
			if GUI.timerIsRunning():
				GUI.stopTimer()
			else:
				GUI.startTimer()
		elif var == "btn2":
			if GUI.timerIsRunning():
				GUI.newLap()
			else:
				GUI.reset()
		else:
			print("No valid command.. TRY AGAIN!")
		root.after(1, checkSerial(GUI))


	root = GUI()
	root.after(100, checkSerial(root))
	root.mainloop()






