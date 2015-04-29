#!/usr/bin/env python

import GUI.GUI as gui
from src.ECUHandler import ECUHandler
import sys, os.path

import threading


gui = gui.GUI()



# Only runs buttonHandler if the software is running on raspbian ("linux2")
if sys.platform == "linux2":
	from src.PhysicalButtonHandler import PhysicalButtonHandler
	#Start to listen for button presses
	#PhysicalButtonHandler = PhysicalButtonHandler(gui)
	#PhysicalButtonHandler.start()

	from src.GPSHandler import GPSHandler
	GPSHandler = GPSHandler()
	GPSHandler.start()

	ECUHandler = ECUHandler(gui, None)
	ECUHandler.start()
else:
	ECUHandler = ECUHandler(gui, None)
	ECUHandler.start()
	print("You're not running this program on Raspberry Pi, button presses will be ignored and GPS will be diabled, continuing...")

gui.mainloop()