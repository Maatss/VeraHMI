#!/usr/bin/env python

from Tkinter import *

class GPS_ECU_status(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.connectedColor = "green"
		self.notConnectedColor = "red"
		self.GPSConnected = False
		self.ECUConnected = False
		self.bgColor = "black"
		self.GPS_label = Label(self, text="GPS", font = ('times', 24, 'bold'), fg="red", bg=self.bgColor)
		self.ECU_label = Label(self, text="ECU", font = ('times', 24, 'bold'), fg="red", bg=self.bgColor)
		self.splitLine = Label(self, text="|", font = ('times', 40), fg="white", bg=self.bgColor)
		self.GPS_label.pack(side=LEFT)
		self.splitLine.pack(side=LEFT)
		self.ECU_label.pack(side=RIGHT)
		self.config(bg=self.bgColor)
		
	def GPS_connected(self, trueOrFalse):
		if trueOrFalse:
			self.GPS_label.config(fg=self.connectedColor)
			self.GPSConnected = True
		else:
			self.GPS_label.config(fg=self.notConnectedColor)
			self.GPSConnected = False

	def isGPSConnected(self):
		return self.GPSConnected

	def isECUConnected(self):
		return self.ECUConnected
			
	def ECU_connected(self, trueOrFalse):
		if trueOrFalse:
			self.ECU_label.config(fg=self.connectedColor)
			self.ECUConnected = True
		else:
			self.ECU_label.config(fg=self.notConnectedColor)
			self.ECUConnected = False
		

#######################################################################################
################################ If running as main ###################################
#######################################################################################
		
if __name__ == '__main__':
	
	root = Tk()
	root.title("Status test")
	GPS_ECU_status().pack()
	root.mainloop()
