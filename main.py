#!/usr/bin/env python

from src.ECUHandler import ECUHandler
from src.MySQLConnection import MySQLConnection
from GUI.GUI import GUI
import sys, threading, thread

try:
	mysql = MySQLConnection()
	mysql_hmi = MySQLConnection()
	gui = GUI(mysql_hmi)
	gui.start_fullscreen()
	threadLock = threading.Lock()

	# Only runs buttonHandler if the software is running on raspbian ("linux2")
	if sys.platform == "linux2":
		
		# Live data thread
		from src.LiveData import LiveData
		liveData = LiveData()
		liveData.streaming = True
		liveData.start()

		#Set time according to GPS
		import gpstime
		thread.start_new_thread(gpstime.setTImeFromGPS, (2,))

		#initalize GPS
		from src.GPSHandler import GPSHandler
		GPSHandler = GPSHandler(gui)
		GPSHandler.start()
		gui.setGPS(GPSHandler)

		#Speedometer Init
		from src.Speedometer import Speedometer
		speedometer = Speedometer(gui, liveData)
		speedometer.start()

		#Initialize ECUHandler
		ECUHandler = ECUHandler(gui, GPSHandler, mysql, False, threadLock, speedometer, liveData)
		ECUHandler.start()

		# Handle button presses 
		from src.ButtonHandler import ButtonHandler
		buttonHandler = ButtonHandler(gui, mysql, threadLock)
		buttonHandler.start()
	else:

		#If this is running on other systems than Raspbian only the ECUHandler will be able to run
		ECUHandler = ECUHandler(gui, None, mysql, False, threadLock)
		ECUHandler.start()
		print("You're not running this program on Raspberry Pi, button presses will be ignored and GPS will be disabled, continuing...")
	
	#Start gui and enter its main loop
	gui.mainloop()
	
except (KeyboardInterrupt, SystemExit):
	print("Exiting...")
	sys.exit()
