#!/usr/bin/env python

from Tkinter import *

class Speed(Frame):
    
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.bgColor = "black"
        self.fgColor = "white"
        self.speed = 0
        self.meanSpeed = 0
        self.speedLabel = Label(self, text="0 (0)", font=('times', 60, 'bold'), bg = self.bgColor, fg = self.fgColor)
        self.speedLabel.pack(side=TOP, anchor=W)
        
        #self.meanSpeedLabel = Label(self, text="0", font=('times', 40, 'bold'), bg = self.bgColor, fg = self.fgColor)
        #self.meanSpeedLabel.pack(side=TOP, anchor=W)
        self.config(bg=self.bgColor)
		
    def setSpeed(self, speed):
		self.speed=float(speed)
		if self.meanSpeed == 0:
			self.meanSpeed = self.speed
		else:
			self.meanSpeed = (self.speed + self.meanSpeed) / 2
			
		self.speedLabel.config(text=str('%.1f' % self.speed) + " (" + str('%.1f' % self.meanSpeed) + ")" )
		
		#self.meanSpeedLabel.config(text=str(meanSpeed))

if __name__ =='__main__':
	root = Tk()
	Speed().pack()
	root.mainloop()
