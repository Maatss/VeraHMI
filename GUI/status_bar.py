#!/usr/bin/env python

from Tkinter import *

class Status_bar(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.bgColor = "black"
		self.fgColor = "white"
		self.modules = ["GPSHandler", "ECUHandler", "StopWatch"]
		self.label = Label(self, text="", font = ('times', 20), fg=self.fgColor, bg=self.bgColor)
		self.label.pack()
		self.config(bg=self.bgColor)
		
	def set_status(self,level, module, message):
		self.label.config(text=self.modules[module - 1] + " - " + message)

        
#######################################################################################
################################ If running as main ###################################
#######################################################################################
#This looks like crap when run as main due tue the fact that there is nothing in the gui at runtime
if __name__ =='__main__':
	root = Tk()
	Status_bar().pack()
	root.mainloop()