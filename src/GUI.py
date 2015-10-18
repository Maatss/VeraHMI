#!/usr/bin/env python

from Tkinter import *
from math import *
import sys

class GUI(Tk):

   def __init__(self):
      Tk.__init__(self)
      
      # Define range of speedometer and rpm display
      self.maxSpeed  = 45
      self.maxRPM    = 5500 

      #Setup screen
      self.width, self.height = 640, 480
      self.config(bg="black")
      self.bind('<Escape>', lambda x: self.attributes("-fullscreen", False))
      self.bind('<space>', lambda x: self.attributes("-fullscreen", True))
      self.bind('<q>', lambda x: sys.exit())
      self.minsize(self.width, self.height)
      self.title("Vera HMI")
      if sys.platform == "linux2":
         self.attributes("-fullscreen", True)
         self.config(cursor="none")
      self.columnconfigure(3, weight=1)
      self.rowconfigure(3, weight=1)

      #Define colors
      self.orange_color = '#F38A1D'
      self.blue_color   = '#36CCFB'
      self.grey_color   = "white"
      self.bgColor      = "black"
      self.fgColor      = "white"
      self.circleColor  = "white"
      self.redColor     = "#EE2B2E"
      self.greenColor   = "#138C03"
      self.yellowColor  = "yellow"

      # Define font properties
      self.fontFamily      = "gotham"
      self.smallFontSize   = 16
      self.mediumFontSize  = 30
      self.largeFontSize   = 50
      self.largerFontSize  = 70


      # Initiate temperatures
      self.tempTopplock = 0
      self.tempMotor     = 0
      self.tempCylinder = 0

      # Define angle for speedometer
      self.startAngleSpeed = -8*pi/10-3*pi/180
      self.speedAngleRange = -self.startAngleSpeed
      
      self.canvas = Canvas(self, width=self.width-10, height=self.height-10, highlightthickness=0, bg=self.bgColor)
      self.canvas.grid(row=1, column=1, sticky=S, rowspan=3, columnspan=3)

      # Define center of canvas and outer limit of gui
      self.x0 = self.width/2;    lx = 9*self.width/20
      self.y0 = self.height/2;   ly = 9*self.height/20

      # Define line widths
      self.smallLineWidth  = 4
      self.mediumLineWidth = 5
      self.largeLineWidth  = 8
      self.largerLineWidth = 16

      # Define different radius
      self.r0 = 0.65 *  min(lx,ly)  # radius of inner circle   
      self.r1 = 0.77 *  min(lx,ly)  # distance of labels from center           
      self.r2 = 0.95 *  min(lx,ly)  # radius for the smaller speed markers
      self.r3 = 0.92 *  min(lx,ly)  # radius for the medium speed markers
      self.r4 = 0.90 *  min(lx,ly)  # radius for the larger speed markers
      self.r5 =         min(lx,ly)  # outer circle

      # Initiate varibles
      self.currentLap = 1

      # Creates white circles for visual effects
      a = self.r5+self.largerLineWidth+self.mediumLineWidth/2

      # label for the lap number
      self.lapNumberLabel = self.canvas.create_text(self.width*9/10, self.height*1/10, fill=self.fgColor, font=(self.fontFamily, self.largerFontSize), text=self.currentLap)


      # label for the temperatures
      self.toppTemp     = self.canvas.create_text(self.width*1/40, self.y0+self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")
      self.cylinderTemp = self.canvas.create_text(self.width*1/40, self.y0,                  anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")
      self.motorTemp    = self.canvas.create_text(self.width*1/40, self.y0-self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")



      # Creates the speed label and speed markers 
      self.drawLinesInCircle(self.maxSpeed, 1, True)

      # Creates the speed label and speed markers 
      rpmLoop = self.maxRPM/100
      self.drawLinesInCircle(rpmLoop, 10, False)

      # Draws the line that separates Speed and RPM at angle 0
      self.canvas.create_line(self.x0, self.y0-self.r1-2*self.largeLineWidth, self.x0, self.y0-self.r5-self.largerLineWidth, fill=self.circleColor, width=self.mediumLineWidth+1)

      # Lables for the timer
      self.totalTimeLabel = self.canvas.create_text(self.x0, self.y0, fill=self.fgColor, font=(self.fontFamily, self.largerFontSize), text="00:00")
      self.currentLapTimeLabel = self.canvas.create_text(self.x0, self.y0+(2*self.r1/5), fill=self.fgColor, font=(self.fontFamily, self.largeFontSize), text="00:00")
   
      # Labels for GPS and ECU
      self.GPS_ECU_angle = -89*pi/180
      self.gpsLabel = self.canvas.create_text(self.x0-(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=E, fill=self.redColor, font=(self.fontFamily, self.mediumFontSize), text="GPS")
      self.ecuLabel = self.canvas.create_text(self.x0+(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=W, fill=self.redColor, font=(self.fontFamily, self.mediumFontSize), text="ECU")
     
      # Creates km/h label
      self.canvas.create_text(self.x0, self.y0-(5*self.r5/20), fill=self.fgColor, font=(self.fontFamily, self.smallFontSize), text="km/h")
      # initiates Speed graphics and labels to None objects
      self.speedLabel = None;    self.meanSpeedArrow = None;     self.speedArrow = None;        self.speedArc = None;
     
      # Initiates RPM graphics and labels
      self.rpmArrow   = None;    self.rpmArc = None;

      self.setSpeedVariables(0, 0)
      self.setRPM(0)







#############################################################################################################################
################################## Internal functions ##########################################################################
#############################################################################################################################

   def drawLinesInCircle(self, maxValue, deliminator, speedOrRPM): # speedOrRPM is ssrt to true when speed is drawn
      for i in range(0,maxValue+1):
         if speedOrRPM:
            phi = self.startAngleSpeed + self.speedAngleRange/maxValue * i
         else:
            phi = self.speedAngleRange/maxValue * (maxValue-i)

         # One lable every 10:th value and no label at zero
         if i%10 == 0 and i != 0:   
            x  = self.x0 + self.r1  * sin(phi)
            y  = self.y0 - self.r1  * cos(phi)
            x1 = self.x0 + self.r4  * sin(phi)
            y1 = self.y0 - self.r4  * cos(phi)
            self.canvas.create_text(x, y, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text=str(i/deliminator))

         elif i%5 == 0:                   # Large line at every 5:th value
            x1 = self.x0 + self.r3 * sin(phi)
            y1 = self.y0 - self.r3 * cos(phi)
         
         else:                            #small speed markers
            x1 = self.x0 + self.r2 * sin(phi)
            y1 = self.y0 - self.r2 * cos(phi)

         if i == 0:
            x2 = self.x0 + (self.r5+self.largeLineWidth+4) * sin(phi)
            y2 = self.y0 - (self.r5+self.largeLineWidth+4) * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.fgColor, width=self.smallLineWidth)

         elif i == maxValue:
            break

         else:
            x2 = self.x0 + self.r5 * sin(phi)
            y2 = self.y0 - self.r5 * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.blue_color, width=self.smallLineWidth)


#############################################################################################################################
################################## Class functions ##########################################################################
#############################################################################################################################

   def setSpeedVariables(self, speed, meanSpeed):
      speed = float(speed)
      meanSpeed = float(meanSpeed)

      #Delete already drawn objects
      self.canvas.delete(self.speedArrow) 
      self.canvas.delete(self.speedLabel)   
      self.canvas.delete(self.speedArc) 
      self.canvas.delete(self.meanSpeedArrow)

      # Draw mean speed line
      meanAngle = self.startAngleSpeed + (self.speedAngleRange/self.maxSpeed)*meanSpeed
      if meanAngle>self.startAngleSpeed + self.speedAngleRange-1.5*pi/180:
         meanAngle = self.startAngleSpeed + self.speedAngleRange-1.5*pi/180
      elif meanAngle < self.startAngleSpeed:
         meanAngle = self.startAngleSpeed

      x1 = self.x0 +  self.r0                         * sin(meanAngle)
      y1 = self.y0 -  self.r0                         * cos(meanAngle)
      x2 = self.x0 + (self.r5 + self.largerLineWidth/2) * sin(meanAngle)
      y2 = self.y0 - (self.r5 + self.largerLineWidth/2) * cos(meanAngle)  
      self.meanSpeedArrow = self.canvas.create_line(x1, y1, x2, y2, dash=4, fill=self.yellowColor, width=self.smallLineWidth) 

      # draw speed line
      phi = self.startAngleSpeed + self.speedAngleRange/self.maxSpeed*speed
      if phi>self.startAngleSpeed + self.speedAngleRange-1.5*pi/180:
         phi = self.startAngleSpeed + self.speedAngleRange-1.5*pi/180
      elif phi < self.startAngleSpeed:
         phi = self.startAngleSpeed

      x1 = self.x0 +  self.r0                         * sin(phi)
      y1 = self.y0 -  self.r0                         * cos(phi)
      x2 = self.x0 + (self.r5 + self.largerLineWidth) * sin(phi)
      y2 = self.y0 - (self.r5 + self.largerLineWidth) * cos(phi)                             
      self.speedLabel = self.canvas.create_text(self.x0, self.y0-(9*self.r5/20), font=(self.fontFamily, self.largerFontSize, 'bold'), fill=self.fgColor, text=str('%.0f' % speed))
      self.speedArrow = self.canvas.create_line(x1, y1, x2, y2, fill=self.orange_color, width=self.smallLineWidth)
      self.speedArc   = self.canvas.create_arc(self.x0-self.r5-self.largerLineWidth/2, self.y0-self.r5-self.largerLineWidth/2, self.x0+self.r5+self.largerLineWidth/2, self.y0+self.r5+self.largeLineWidth/2, outline=self.orange_color, extent=(-self.startAngleSpeed+phi)*(180/pi), style=ARC, width=self.largerLineWidth, start=90-(phi*180/pi))
      
      

   def setRPM(self, rpm):

      phi = self.speedAngleRange - self.speedAngleRange/5500*rpm
      if phi<0:
         phi = 1.5*pi/180
      elif phi > self.speedAngleRange:
         phi = self.speedAngleRange-1.5*pi/180
      x1 = self.x0 +  self.r0                         * sin(phi)
      y1 = self.y0 -  self.r0                         * cos(phi)
      x2 = self.x0 + (self.r5 + self.largerLineWidth) * sin(phi)
      y2 = self.y0 - (self.r5 + self.largerLineWidth) * cos(phi) 
      self.canvas.delete(self.rpmArrow)   
      self.canvas.delete(self.rpmArc)                              
      self.rpmArrow = self.canvas.create_line(x1, y1, x2, y2, fill=self.blue_color, width=self.smallLineWidth)
      self.rpmArc = self.canvas.create_arc(self.x0-self.r5-self.largerLineWidth/2, self.y0-self.r5-self.largerLineWidth/2, self.x0+self.r5+self.largerLineWidth/2, self.y0+self.r5+self.largeLineWidth/2, outline=self.blue_color, extent=-(self.startAngleSpeed+phi)*(180/pi), style=ARC, width=self.largerLineWidth, start=90-self.speedAngleRange*180/pi)




   def reset(self):
      self.meanSpeed = 0
      self.numberOfDataPoints = 0
      self.totalSpeed = 0
      self.setSpeedVariables(float(self.canvas.itemcget(self.speedLabel, 'text')), 0)

      # Reset lapnumber
      self.canvas.delete(self.lapNumberLabel) 
      self.currentLap = 1
      self.lapNumberLabel = self.canvas.create_text(self.width*9/10, self.height*1/10, fill=self.fgColor, font=(self.fontFamily, self.largerFontSize), text=self.currentLap)


   def newLap(self):
      self.canvas.delete(self.lapNumberLabel) 
      self.currentLap += 1
      self.lapNumberLabel = self.canvas.create_text(self.width*9/10, self.height*1/10, fill=self.fgColor, font=(self.fontFamily, self.largerFontSize), text=self.currentLap)

   def connectGPS(self):
      self.canvas.delete(self.gpsLabel)   
      self.gpsLabel = self.canvas.create_text(self.x0-(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=E, fill=self.greenColor, font=(self.fontFamily, self.mediumFontSize), text="GPS")
     
   def disconnectGPS(self):
      self.canvas.delete(self.gpsLabel)   
      self.gpsLabel = self.canvas.create_text(self.x0-(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=E, fill=self.redColor, font=(self.fontFamily, self.mediumFontSize), text="GPS")
     
   def connectECU(self):
      self.canvas.delete(self.ecuLabel)   
      self.ecuLabel = self.canvas.create_text(self.x0+(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=W, fill=self.greenColor, font=(self.fontFamily, self.mediumFontSize), text="ECU")
     
   def disconnectECU(self):
      self.canvas.delete(self.ecuLabel)   
      self.ecuLabel = self.canvas.create_text(self.x0+(self.r1*cos(self.GPS_ECU_angle)), self.y0-(self.r1*sin(self.GPS_ECU_angle)), anchor=W, fill=self.redColor, font=(self.fontFamily, self.mediumFontSize), text="ECU")
      self.canvas.delete(self.toppTemp)
      self.toppTemp     = self.canvas.create_text(self.width*1/40, self.y0+self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")
      self.canvas.delete(self.cylinderTemp)     
      self.cylinderTemp = self.canvas.create_text(self.width*1/40, self.y0,                  anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")
      self.canvas.delete(self.motorTemp)
      self.motorTemp    = self.canvas.create_text(self.width*1/40, self.y0-self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text="--")
  
   def setStatus(self, level, module, message):
      pass

   def setTemperatures(self, tempTopplock, tempMotor, tempCylinder):
      self.tempTopplock = tempTopplock
      self.tempCylinder = tempCylinder
      self.tempMotor    = tempMotor


      self.canvas.delete(self.toppTemp)
      self.toppTemp     = self.canvas.create_text(self.width*1/40, self.y0+self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text=str(self.tempTopplock))
      self.canvas.delete(self.cylinderTemp)
      self.cylinderTemp = self.canvas.create_text(self.width*1/40, self.y0,                  anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text=str(self.tempCylinder))
      self.canvas.delete(self.motorTemp)
      self.motorTemp    = self.canvas.create_text(self.width*1/40, self.y0-self.height*3/20, anchor=W, fill=self.fgColor, font=(self.fontFamily, self.mediumFontSize), text=str(self.tempMotor))


   def setStopWatchVariables(self, totalTime, currentLapTime):
      self.canvas.delete(self.totalTimeLabel)
      self.canvas.delete(self.currentLapTimeLabel)
      self.totalTimeLabel = self.canvas.create_text(self.x0, self.y0, fill=self.fgColor, font=(self.fontFamily, self.largerFontSize), text=totalTime)
      self.currentLapTimeLabel = self.canvas.create_text(self.x0, self.y0+(2*self.r1/5), fill=self.fgColor, font=(self.fontFamily, self.largeFontSize), text=currentLapTime)
   



# main
if __name__ =='__main__':

   def checkSerial(GUI):
      var = raw_input("Enter command: " )
      if var == "stop":
         GUI.stopTimer()
      elif var == "lap":
         GUI.newLap()
      elif var == "start":
         GUI.startTimer()
      elif var == "gpsOn":
         GUI.connectGPS()
      elif var == "gpsOff":
         GUI.disconnectGPS()
      elif var == "ecuOn":
         GUI.connectECU()
      elif var == "ecuOff":
         GUI.disconnectECU()
      elif var == "status":
         level = raw_input("Enter level: ")
         module = raw_input("enter module number: ")
         string = raw_input("Enter status: ")
         GUI.setStatus(level, module, string)
      elif var == "q":
         print("q was pressed")
         sys.exit()
      elif var == "speed":
         spd = raw_input("Enter speed: ")
         GUI.setSpeedVariables(float(spd), float(spd)/2)
      elif var == "rpm":
         r = raw_input("Enter RPM: ")
         GUI.setRPM(float(r))
      elif var == "btn1":
         if GUI.timerIsRunning():
            GUI.stopTimer()
         else:
            GUI.startTimer()
      elif var == "btn2":
         if GUI.timerIsRunning():
            GUI.newLap()
         else:
            GUI.reset()
      elif var == "reset":
         GUI.reset()
      else:
         print("No valid command.. TRY AGAIN!")
      root.after(1, checkSerial(GUI))

      GUI.after(1, checkSerial(GUI))
 
   root = GUI() 
   root.after(1, checkSerial(root))
   root.mainloop()



