#!/usr/bin/env python

from Tkinter import *

#Import our own modules/objects
from timer import TimerFrame
from status_bar import Status_bar
from GPS_ECU_status import GPS_ECU_status
from Speed import Speed
from RPM import RPM
import time, sys

sys.path.append('/home/pi/VeraHMI/src')
from src.MySQLConnection import MySQLConnection


class GUI(Tk):

	def __init__(self, mysql = None):
		Tk.__init__(self)

		self.mysql = mysql
		self.gps = None
		#Setup screen
		self.width, self.height = 500, 300
		self.config(bg="black")
		self.bind('<Escape>', self.end_fullscreen)
		self.bind('<space>', self.start_fullscreen)
		self.minsize(self.width, self.height)
		self.columnconfigure(3, weight=1)
		self.rowconfigure(3, weight=1)
		self.title("Vera HMI")

		#center screen 
		x = (self.winfo_screenwidth() / 2) - (self.width / 2)
		y = (self.winfo_screenheight() / 2) - (self.height / 2)
		self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

		#GPS and ECU Status
		self.GPS_ECU_status = GPS_ECU_status()
		self.GPS_ECU_status.grid(row=0, column=3, sticky=E)
		self.GPS_ECU_status.config(padx=10)

		#Timer
		self.timer = TimerFrame()
		self.timer.grid(row=3, column=2, columnspan=2, rowspan=2, sticky=SE)
		self.timer.config(padx=20, pady=10)

		# Status
		self.status = Status_bar()
		self.status.config(padx=10)
		self.status.grid(row=0, column=0, columnspan=3, sticky=W)

		# Speed
		self.speed = Speed()
		self.speed.grid(row=3, column=0, sticky=SW)
		self.speed.config(padx=20, pady=10)

		# RPM
		self.rpm = RPM()
		self.rpm.grid(row=4, column=0, sticky=SW)
		self.rpm.config(padx=20, pady=10)

	def stopTimer(self):
		self.timer.stopCount()
		self.setStatus(1, 3, "Stopped")

	def timerIsRunning(self):
		return self.timer.isRunning()

	def reset(self):
		self.timer.reset()
		self.speed.reset()
		self.setStatus(1, 3, "Reset timer")

	def newLap(self):
		self.timer.newLap()
		self.setStatus(1, 3, "New lap")

	def startTimer(self):
		self.timer.startCount()
		self.setStatus(1, 3, "Started")

	def connectGPS(self):
		self.GPS_ECU_status.GPS_connected(True)
		#self.saveHMILog(1, 1, "Connected")

	def disconnectGPS(self):
		self.GPS_ECU_status.GPS_connected(False)
		#self.saveHMILog(1, 1, "Disconnected")

	def connectECU(self):
		self.GPS_ECU_status.ECU_connected(True)
		self.saveHMILog(1, 2, "Connected")

	def disconnectECU(self):
		self.GPS_ECU_status.ECU_connected(False)
		self.saveHMILog(1, 2, "Disconnected")

	def saveHMILog(self, level, module, message):
		#modules: 1=GPSHAndler, 2=ECUHandler, 3=StopWatch
		if sys.platform == "linux2" and self.gps != None:
			(lat, lon, speed) = self.gps.getGPSPos()
		else:
			(lat, lon, speed) = (None, None, None)
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
	else:
		print("No valid command.. TRY AGAIN!")
	root.after(1, checkSerial(GUI))


if __name__ == '__main__':
	root = GUI()
	root.after(100, checkSerial(root))
	root.mainloop()
