#!/usr/bin/env python

from src.GUI import GUI
from src.ECUHandler import ECUHandler
import sys, threading, time, thread, os


def initClasses():

	# SpeedHandler
	from src.SpeedHandler import SpeedHandler
	speedHandler = SpeedHandler(environment)
	speedHandler.start()

	# ECUHandler
	ecuHandler = ECUHandler(environment)
	ecuHandler.start()

	# ButtonHandler
	from src.ButtonHandler import ButtonHandler
	buttonHandler = ButtonHandler(environment)
	buttonHandler.start()

	# GPSHandler
	from src.GPSHandler import GPSHandler
	gpsHandler = GPSHandler(environment)
	gpsHandler.start()

	# Restart 4g router 
	#os.system('sudo ifdown usb0')
	#time.sleep(0.5)
	#os.system('sudo ifup usb0')


try:
	# Only runs buttonHandler if the software is running on raspbian ("linux2")
	if sys.platform == "linux2":

		#Set time according to GPS
		from src import gpstime
		thread.start_new_thread(gpstime.setTImeFromGPS, (2,))

		# Environment
		from src.Environment import Environment
		environment = Environment()
		environment.start()

		gui = GUI(environment)

		thread.start_new_thread(initClasses, ())


		
	else:
		def checkSerial(GUI):
			var = raw_input("Enter command: " )
			if var == "stop":
				GUI.stopTimer()
			elif var == "lap":
				GUI.newLap()
			elif var == "start":
				GUI.startTimer()
			elif var == "gpsOn":
				GUI.connectGPS()
			elif var == "gpsOff":
				GUI.disconnectGPS()
			elif var == "ecuOn":
				GUI.connectECU()
			elif var == "ecuOff":
				GUI.disconnectECU()
			elif var == "status":
				level = raw_input("Enter level: ")
				module = raw_input("enter module number: ")
				string = raw_input("Enter status: ")
				GUI.setStatus(level, module, string)
			elif var == "q":
				print("q was pressed")
				sys.exit()
			elif var == "speed":
				spd = raw_input("Enter speed: ")
				GUI.setSpeedVariables(float(spd), float(spd)/2)
			elif var == "rpm":
				r = raw_input("Enter RPM: ")
				GUI.setRPM(float(r))
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
			elif var == "reset":
				GUI.reset()
			elif var == "temp":
				temp1 = raw_input("Enter head temp: ")
				temp2 = raw_input("Enter motor temp: ")
				temp3 = raw_input("Enter cylinder temp: ")
				GUI.setTemperatures(temp1, temp2, temp3)
			else:
				print("No valid command.. TRY AGAIN!")
			GUI.after(1, checkSerial(GUI))
			
		print("You are not running this program on Raspberry Pi, entering debug mode...")
		checkSerial(gui)
		
	
	#Start gui and enter its mainloop
	gui.start()
	
except (KeyboardInterrupt, SystemExit):
	print("Exiting...")
	sys.exit()



