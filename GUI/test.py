#!/usr/bin/env python

from Tkinter import *

#Import our own modules/objects
from timer import TimerFrame
from status_bar import Status_bar
from GPS_ECU_status import GPS_ECU_status
from Speed import Speed
from RPM import RPM


def checkSerial():
	var = raw_input("Enter command: " )
	if var == "stop":
		timer.stopCount()
	elif var == "lap":
		timer.newLap()
	elif var == "start":
		timer.startCount()
	elif var == "GPS_ON":
		GPS_ECU_status.GPS_connected(True)
	elif var == "GPS_OFF":
		GPS_ECU_status.GPS_connected(False)
	elif var == "ECU_ON":
		GPS_ECU_status.ECU_connected(True)
	elif var == "ECU_OFF":
		GPS_ECU_status.ECU_connected(False)
	elif var == "status":
		level = raw_input("Enter level: ")
		module = raw_input("enter module number: ")
		string = raw_input("Enter status: ")
		status.set_status(int(level), int(module), string)
	elif var == "q":
		root.quit()
	elif var == "speed":
		spd = raw_input("Enter speed: ")
		speed.setSpeed(spd)
	elif var == "rpm":
		r = raw_input("Enter RPM: ")
		rpm.setRPM(r)
	else:
		print("No valid command.. TRY AGAIN!")
	root.after(1, checkSerial)

def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)

def start_fullscreen(event=None):
    root.attributes("-fullscreen", True)

width, height = 500, 300
root = Tk()
root.config(bg="black")
root.bind('<Escape>', end_fullscreen)
root.bind('<space>', start_fullscreen)
root.minsize(width, height)
#root.maxsize(width, height)

root.columnconfigure(3, weight=1)
root.rowconfigure(3, weight=1)

#center screen 

x = (root.winfo_screenwidth() / 2) - (width / 2)
y = (root.winfo_screenheight() / 2) - (height / 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))



#GPS and ECU Status
GPS_ECU_status = GPS_ECU_status()
GPS_ECU_status.grid(row=0, column=3, sticky=E)
GPS_ECU_status.config(padx=10)

#Timer
timer = TimerFrame()
timer.grid(row=3, column=2, columnspan=2, rowspan=2, sticky=SE)
timer.config(padx=20, pady=10)

# Status
status = Status_bar()
status.config(padx=10)
status.grid(row=0, column=0, columnspan=3, sticky=W)
status.set_status(1, 0, "Session started")

# Speed
speed = Speed()
speed.grid(row=3, column=0, sticky=SW)
speed.config(padx=20, pady=10)

# RPM
rpm = RPM()
rpm.grid(row=4, column=0, sticky=SW)
rpm.config(padx=20, pady=10)


root.attributes("-fullscreen", False)
root.after(100, checkSerial)
root.mainloop()
