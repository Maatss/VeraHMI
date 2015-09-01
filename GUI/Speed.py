#!/usr/bin/env python

from Tkinter import *

class Speed(Frame):
    
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.bgColor = "black"
        self.fgColor = "white"
        self.speed = 0
        self.meanSpeed = 0
        self.numberOfDataPoints = 0
        self.totalSpeed = 0
        self.speedLabel = Label(self, text="0 (0)", font=('times', 50, 'bold'), bg = self.bgColor, fg = self.fgColor)
        self.speedLabel.pack(side=TOP, anchor=W)
        
        #self.meanSpeedLabel = Label(self, text="0", font=('times', 40, 'bold'), bg = self.bgColor, fg = self.fgColor)
        #self.meanSpeedLabel.pack(side=TOP, anchor=W)
        self.config(bg=self.bgColor)
		
    def setSpeed(self, speed):
		self.speed=float(speed)
		self.numberOfDataPoints += 1
		self.totalSpeed += self.speed
		self.meanSpeed = self.totalSpeed / self.numberOfDataPoints
		self.speedLabel.config(text=str('%.0f' % self.speed) + " (" + str('%.0f' % self.meanSpeed) + ")" )
		
		#self.meanSpeedLabel.config(text=str(meanSpeed))
    def reset(self):
        self.meanSpeed = 0
        self.numberOfDataPoints = 0
        self.speedLabel.config(text="0" + " (0)")


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ =='__main__':
	root = Tk()
	Speed().pack()
	root.mainloop()
