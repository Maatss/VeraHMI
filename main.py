#!/usr/bin/env python

from src.ECUHandler import ECUHandler
from src.MySQLConnection import MySQLConnection
from GUI.GUI import GUI
import sys, threading

try:
	mysql = MySQLConnection()
	mysql_hmi = MySQLConnection()
	gui = GUI(mysql_hmi)
	gui.start_fullscreen()

	# Only runs buttonHandler if the software is running on raspbian ("linux2")
	if sys.platform == "linux2":
		#initalize GPS
		from src.GPSHandler import GPSHandler
		GPSHandler = GPSHandler(gui)
		GPSHandler.start()
		gui.setGPS(GPSHandler)

		#Initialize ECUHandler
		ECUHandler = ECUHandler(gui, GPSHandler, mysql, debug=True)
		ECUHandler.start()

		# Handle button presses 
		from src.ButtonHandler import ButtonHandler
		buttonHandler = ButtonHandler(gui, mysql)
		buttonHandler.start()
	else:

		#If this is running on other systems than Raspbian only the ECUHandler will be able to run
		ECUHandler = ECUHandler(gui, None, mysql, debug=True)
		ECUHandler.start()
		print("You're not running this program on Raspberry Pi, button presses will be ignored and GPS will be disabled, continuing...")
	
	#Start gui and enter its main loop
	gui.mainloop()
	
except (KeyboardInterrupt, SystemExit):
	print("Exiting...")
	sys.exit()
