#!/usr/bin/env python

from Tkinter import *

class GPS_ECU_status(Frame):
	def __init__(self, parent=None, **options):
		Frame.__init__(self, parent, **options)
		self.connectedColor = "green"
		self.notConnectedColor = "red"
		self.bgColor = "black"
		self.GPS_label = Label(self, text="GPS", font = ('times', 24, 'bold'), fg="red", bg=self.bgColor)
		self.ECU_label = Label(self, text="ECU", font = ('times', 24, 'bold'), fg="red", bg=self.bgColor)
		self.GPS_label.pack(side=LEFT)
		self.ECU_label.pack(side=RIGHT)
		self.config(bg=self.bgColor)
		
	def GPS_connected(self, trueOrFalse):
		if trueOrFalse:
			self.GPS_label.config(fg=self.connectedColor)
		else:
			self.GPS_label.config(fg=self.notConnectedColor)
			
	def ECU_connected(self, trueOrFalse):
		if trueOrFalse:
			self.ECU_label.config(fg=self.connectedColor)
		else:
			self.ECU_label.config(fg=self.notConnectedColor)
		

#######################################################################################
################################ If running as main ###################################
#######################################################################################
		
if __name__ == '__main__':
	
	root = Tk()
	root.title("Status test")
	GPS_ECU_status().pack()
	root.mainloop()
