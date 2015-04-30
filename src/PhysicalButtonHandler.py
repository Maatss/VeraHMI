#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, threading, time, sys
from ButtonHandler import ButtonHandler

class PhysicalButtonHandler(threading.Thread):

	def __init__(self, gui = None):
		threading.Thread.__init__(self)
		self.deamon = True
		self.stopStartButton = 36
		self.lapButton = 38
		self.resetButton = 40
		self.gui = gui


	def run(self):
		try:
			stopButtonHandler = ButtonHandler(self.stopStartButton, True, "startStop", self.gui)
			stopButtonHandler.start()

			lapButtonHandler = ButtonHandler(self.lapButton, True, "lap", self.gui)
			lapButtonHandler.start()
			
		except (KeyboardInterrupt, SystemExit):
			self.quit()
			self._Thread__stop()



if __name__ =='__main__':
	try:
		item = PhysicalButtonHandler()
		item.start()
	except (KeyboardInterrupt, SystemExit):
		sys.exit()
