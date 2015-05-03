#!/usr/bin/env python

from Tkinter import *
from time import *

class TimerFrame(Frame):
    
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.bgColor = "black"
        self.fgColor = "white"
        self.label = Label(self, text="00:00", font=('times', 80, 'bold'), bg=self.bgColor, fg=self.fgColor)
        self.label.pack(side=TOP)
        self.config(bg=self.bgColor)
        # Number of laps frame
        (self.currLapFrame, dontCare, self.lapsLabel) = self.createTimeFrame("Current lap:", "1", 30)
        
        # lap frames
        (lap2Frame, self.lap2Label, self.lap2) = self.createTimeFrame("-", "--:--", 30)
        (lap1Frame, self.lap1Label, self.lap1) = self.createTimeFrame("1.", "00:00", 40)
        self.lap2Label.config(font=('times', 30, 'bold'), bg=self.bgColor, fg=self.fgColor)
        self.lap1Label.config(font=('times', 40, 'bold'), bg=self.bgColor, fg=self.fgColor)
        
        self.seconds = 0
        self.minutes = 0
        self.laps = 1
        self.timeSinceLastLap = 0
        self.stopped = True
        self.after(1000, self.updateClock)


    def createTimeFrame(self, leftText, rightText, fontSize):
        frame = Frame(self, bg=self.bgColor)
        frame.pack(side=BOTTOM, fill=X)
        leftLabel = Label(frame, text=leftText, font=('times', fontSize), bg=self.bgColor, fg=self.fgColor)
        leftLabel.pack(side=LEFT)
        rightLabel = Label(frame, text=rightText, font=('times', fontSize), bg=self.bgColor, fg=self.fgColor)
        rightLabel.pack(side=RIGHT)
        return (frame, leftLabel, rightLabel)
    
    
    # update clock
    def updateClock(self):
        if self.stopped == False:
            self.seconds += 1
        
            if self.seconds >= 60:
                self.minutes += 1
                self.seconds = 0
            string = self.toString(self.minutes, self.seconds)
            self.label.config(text=string)
            currLapTime = (self.minutes*60 + self.seconds)-self.timeSinceLastLap
            lapMinutes = currLapTime//60
            lapSeconds = currLapTime - lapMinutes*60
            string2 = self.toString(lapMinutes, lapSeconds)
            #print("Total time: " + string + " Lap time: " + string2)
            self.lap1.config(text=string2)

        self.after(1000, self.updateClock)

    #get time as string
    def toString(self, minutes, seconds):
        if minutes >= 10:
            string = str(minutes)
        else:
            string = "0" + str(minutes)

        string += ":"

        if seconds >= 10:
            string += str(seconds)
        else:
            string += "0" + str(seconds)
        return string

    # stop counting
    def stopCount(self):
        self.stopped = True

    # start counting
    def startCount(self):
        self.stopped = False
        
    def isRunning(self):
        return not self.stopped

    def newLap(self):
        self.laps += 1
        self.lap2.config(text=self.lap1.cget('text'))
        self.lap2Label.config(text=self.lap1Label.cget('text'))
        
        totalLapTime = (self.minutes*60 + self.seconds)-self.timeSinceLastLap
        self.timeSinceLastLap = self.minutes*60 + self.seconds
        lapMinutes = totalLapTime//60
        lapSeconds = totalLapTime - lapMinutes*60
        string = self.toString(lapMinutes, lapSeconds)
        self.lap1.config(text="00:00")
        self.lap1Label.config(text=str(self.laps)+".")
        self.lapsLabel.config(text=str(self.laps))
        return (string, self.laps-1)

    def reset(self):
        self.seconds = 0
        self.minutes = 0
        self.laps = 1
        self.timeSinceLastLap = 0
        self.stopped = True

        self.label.config(text="00:00")
        
        self.lap1Label.config(text="1.")
        self.lap1.config(text="00:00")
        
        self.lap2Label.config(text="-")
        self.lap2.config(text="--:--")

        self.lapsLabel.config(text="0")


if __name__ == '__main__':
    
    def startOrStop():
        if timer.stopped == True:
            button.config(text="Stop")
            timer.startCount()
        else:
            button.config(text="Start")
            timer.stopCount()


    root = Tk()
    timer = TimerFrame()
    timer.pack()

    reset = Button(root, text="New lap", command=timer.newLap)
    reset.pack(side=BOTTOM, fill=X)
        
    button = Button(root, text="Stop", command=startOrStop)
    button.pack(side=BOTTOM, fill=X)
    
    root.mainloop()
