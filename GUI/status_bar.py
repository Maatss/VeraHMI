#!/usr/bin/env python

from Tkinter import *

class Status_bar(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.bgColor = "black"
		self.fgColor = "white"
		self.modules = ["GPSHandler", "ECUHandler", "StopWatch"]
		self.label = Label(self, text="Status: ", font = ('times', 20), fg=self.fgColor, bg=self.bgColor)
		self.label.pack()
		self.config(bg=self.bgColor)
		
	def set_status(self,level, module, message):
		self.label.config(text="Status: " + self.modules[module - 1] + " - " + message)
		# TODO: implement MySQL connection to insert into HMILog and more...
        # Maybe make the status go away after x seconds?? 

        
