#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, threading, time
import RPi.GPIO as GPIO

class PhysicalButtonHandler(threading.Thread):

	def __init__(self, gui):
		threading.Thread.__init__(self)
		self.stopStartButton = 36
		self.lapButton = 38
		self.resetButton = 40
		self.gui = gui

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.stopStartButton, GPIO.IN)
		GPIO.setup(self.lapButton, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		GPIO.setup(self.resetButton, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	def checkForPress(self):
		if self.gui.timerIsRunning():
			pass
			'''
			print("timer is running")
			if(GPIO.input(self.stopStartButton) ==1):
				self.gui.stopTimer()
				print("timer stopped")
		else:
			if(GPIO.input(self.stopStartButton) ==0):
				self.gui.startTimer()
				'''
	def run(self):
		try:
			while True:
				self.checkForPress()
		except KeyboardInterrupt:
			self.quit()
			self._Thread__stop()