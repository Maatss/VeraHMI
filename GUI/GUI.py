#!/usr/bin/env python

from Tkinter import *

#Import our own modules/objects
from timer import TimerFrame
from status_bar import Status_bar
from GPS_ECU_status import GPS_ECU_status
from Speed import Speed
from RPM import RPM
import time

class GUI(Tk):

	def __init__(self, mysql):
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
		self.status.set_status(1, 0, "Session started")

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

	def timerIsRunning(self):
		return self.timer.isRunning()

	def newLap(self):
		self.timer.newLap()

	def startTimer(self):
		self.timer.startCount()

	def connectGPS(self):
		self.GPS_ECU_status.GPS_connected(True)

	def disconnectGPS(self):
		self.GPS_ECU_status.GPS_connected(False)

	def connectECU(self):
		self.GPS_ECU_status.ECU_connected(True)

	def disconnectECU(self):
		self.GPS_ECU_status.ECU_connected(False)

	def setStatus(self, level, module, message):
		#modules: 1=GPSHAndler, 2=ECUHandler, 3=StopWatch
		self.status.set_status(int(level), int(module), message)
		if sys.platform == "linux2" and self.gps != None:
			(lat, lon, alt, speed) = self.gps.getGPSPos()
		else:
			(lat, lon, alt, speed) = (None, None, None, None)
		date = time.strftime("%Y-%m-%d")
		self.mysql.saveHMILog(date, level, module, message, [lat, lon])

	def setSpeed(self, speed):
		self.speed.setSpeed(speed)

	def setRPM(self, rpm):
		self.rpm.setRPM(rpm)

	def end_fullscreen(self, event=None):
	    self.attributes("-fullscreen", False)

	def start_fullscreen(self, event=None):
	    self.attributes("-fullscreen", True)


	def setMySQL(self, mysql):
		self.mysql = mysql

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
