#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *

class Temp(Frame):

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.bgColor = "black"
        self.fgColor = "white"
        self.topplockTemp = 0
        self.motorTemp = 0
        self.cylinderTemp = 0
        #self.title = Label(self, text="Temperature:", font=('times', 24, 'bold'), bg = self.bgColor, fg = self.fgColor)
        #self.title.pack(side=TOP, anchor=W)
        self.topplockLabel = Label(self, text="Topplock: \t--℃", font=('times', 20), bg = self.bgColor, fg = self.fgColor)
        self.topplockLabel.pack(side=TOP, anchor=W)
        self.motorLabel = Label(self, text="Motor: \t\t--℃", font=('times', 20), bg = self.bgColor, fg = self.fgColor)
        self.motorLabel.pack(side=TOP, anchor=W)
        self.cylinderLabel = Label(self, text="Cylinder: \t--℃", font=('times', 20), bg = self.bgColor, fg = self.fgColor)
        self.cylinderLabel.pack(side=TOP, anchor=W)

        self.config(bg=self.bgColor)

    def setTemp(self, topplockTemp, motorTemp, cylinderTemp):
        self.topplockTemp = topplockTemp
        self.motorTemp = motorTemp
        self.cylinderTemp = cylinderTemp
        self.updateGUI()

    def updateGUI(self):
        self.topplockLabel.config(text="Topplock: \t" + str(self.topplockTemp) + "℃")
        self.motorLabel.config(text="Motor: \t\t" + str(self.motorTemp) + "℃")
        self.cylinderLabel.config(text="Cylinder: \t" + str(self.cylinderTemp) + "℃")

    def reset(self):
        self.topplockLabel.config(text="Topplock: \t--℃")
        self.motorLabel.config(text="Motor: \t\t--℃")
        self.cylinderLabel.config(text="Cylinder: \t--℃")


#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ =='__main__':
    root = Tk()
    Temp().pack()
    root.mainloop()

