#!/usr/bin/env python

from src.ECUHandler import ECUHandler
from src.MySQLConnection import MySQLConnection
from GUI.GUI import GUI

import sys, os.path, threading, os, time

try:
	global gui
	mysql = MySQLConnection()
	mysql_hmi = MySQLConnection(mysql.getID)
	gui = GUI(mysql_hmi)
	time.sleep(1)

	gui.attributes("-fullscreen", True)
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
		buttonHandler = ButtonHandler(gui)
		buttonHandler.start()
	else:
		ECUHandler = ECUHandler(gui, None, mysql)
		ECUHandler.start()
		print("You're not running this program on Raspberry Pi, button presses will be ignored and GPS will be disabled, continuing...")

	gui.mainloop()
	
except (KeyboardInterrupt, SystemExit):
	print("Exiting...")
	sys.exit()
