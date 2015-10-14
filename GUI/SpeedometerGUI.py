#!/usr/bin/env python

from Tkinter import *
from math import *

class SpeedometerGUI(Frame):

   def __init__(self, width, max_number, number_of_labels):
      Frame.__init__(self)
      self.orange_color = '#DE4004'
      self.speed = 0
      self.meanSpeed = 0
      self.numberOfDataPoints = 0
      self.totalSpeed = 0
      self.max_number = max_number+5
      number_of_labels = number_of_labels

      self.speed_start_angle = -8*pi/10
      self.speed_angle_range = -self.speed_start_angle
      self.bgColor = "black"
      self.fgColor = "white"
      self.width = width
      self.height = self.width
      self.canvas = Canvas(self, width=self.width, height=self.height, highlightthickness=0, bg=self.bgColor)
      self.canvas.pack()

      self.x0 = self.width/2; lx = 9*self.width/20              # center and half-width of clock face
      self.y0 = self.height/2; ly = 9*self.height/20
      self.r0 = 0.77 * min(lx,ly)         # distance of labels from center     
      self.r1 = 0.60 * min(lx,ly)                     
      self.r2 = min(lx,ly)                        # length of speedArrow
      r3 = 0.95 * min(lx,ly)
      r4 = 0.90 * min(lx,ly)   
      self.r6 = self.r2+4
      self.r7 =self.r2-2

      self.canvas.create_oval(self.x0-lx-9, self.y0-ly-9, self.x0+lx+9, self.y0+ly+9, outline=self.fgColor, width=4)
      self.canvas.create_oval(self.x0-self.r1, self.y0-self.r1, self.x0+self.r1, self.y0+self.r1, outline=self.fgColor, width=3)

      for i in range(0,self.max_number+1):
         phi = self.speed_start_angle + self.speed_angle_range/self.max_number * i
         if i%10 == 0 and i != 0:   
            x = self.x0 + self.r0 * sin(phi)
            y = self.y0 - self.r0 * cos(phi)
            self.canvas.create_text(x, y, fill=self.fgColor, font=('times', 26, 'bold'), text=str(i))

         if i%5 != 0:
            x1 = self.x0 + r3 * sin(phi)
            y1 = self.y0 - r3 * cos(phi)
         else:
            x1 = self.x0 + r4 * sin(phi)
            y1 = self.y0 - r4 * cos(phi)


         if i == 0:
            x2 = self.x0 + (self.r2+7) * sin(phi)
            y2 = self.y0 - (self.r2+7) * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.orange_color, width=3)
         elif i == self.max_number:
            break
         else:
            x2 = self.x0 + self.r2 * sin(phi)
            y2 = self.y0 - self.r2 * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.orange_color, width=3)

      for j in range(0,56):
         phi = self.speed_angle_range/55 * (55-j)
         if j%10 == 0 and j != 0:   
            x = self.x0 + self.r0 * sin(phi)
            y = self.y0 - self.r0 * cos(phi)
            self.canvas.create_text(x, y, fill="blue", font=('times', 26, 'bold'), text=str(j/10))

         if j%5 != 0:
            x1 = self.x0 + r3 * sin(phi)
            y1 = self.y0 - r3 * cos(phi)
         else:
            x1 = self.x0 + r4 * sin(phi)
            y1 = self.y0 - r4 * cos(phi)


         if j == 0:
            x2 = self.x0 + (self.r2+7) * sin(phi)
            y2 = self.y0 - (self.r2+7) * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3)
         elif j == 55:
            break
         else:
            x2 = self.x0 + self.r2 * sin(phi)
            y2 = self.y0 - self.r2 * cos(phi)
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3)



      y = self.y0-(self.height/8)
      self.canvas.create_line(self.x0, self.y0-self.r1, self.x0, self.y0-ly-9, fill=self.fgColor, width=4)
      x_1 = self.x0 + self.r1 * sin(self.speed_start_angle-2*pi/180)
      y_1 = self.y0 - self.r1 * cos(self.speed_start_angle-2*pi/180)
      x_2 = self.x0 + (self.r6+4) * sin(self.speed_start_angle-2*pi/180)
      y_2 = self.y0 - (self.r6+4) * cos(self.speed_start_angle-2*pi/180)
      self.canvas.create_line(x_1, y_1, x_2, y_2, fill=self.fgColor, width=4)
      self.canvas.create_line(self.x0+(self.x0-x_1), y_1, self.x0+(self.x0-x_2), y_2, fill=self.fgColor, width=4)

      #self.canvas.create_rectangle(self.x0-30, y-16, self.x0+30, y+16, outline=self.fgColor, width=3)
      self.canvas.create_text(self.x0, self.y0-(2*self.r1/3)+22, fill=self.orange_color, font=('times', 16), text="km/h")
      self.canvas.create_text(self.x0, self.y0, fill=self.fgColor, font=('times', 55), text="00:00")
      self.canvas.create_text(self.x0, self.y0+(1*self.r1/2)+6, fill=self.fgColor, font=('times', 38), text="00:00")
      
      #GPS and ECU label
      self.canvas.create_text(self.x0-30, self.y0+108, fill="red", font=('times', 28), text="GPS")
      self.canvas.create_text(self.x0+30, self.y0+108, fill="green", font=('times', 28), text="ECU")
     

      self.speedLabel = self.canvas.create_text(self.x0, self.y0-(2*self.r1/3), font=('times', 44, 'bold'), text="0")
      
      self.speedArrow = self.canvas.create_line(self.x0, self.y0, x, y, fill=self.orange_color, width=4)  
      self.speedArc = self.canvas.create_arc(self.x0-self.r2-3, self.y0-self.r2-3, self.x0+self.r2+3, self.y0+self.r2+3, outline=self.orange_color, extent=20, style=ARC, width=8, start=180)
      
      self.rpmArrow = self.canvas.create_line(self.x0, self.y0, x, y, fill=self.orange_color, width=4)  
      self.rpmArc = self.canvas.create_arc(self.x0-self.r2-3, self.y0-self.r2-3, self.x0+self.r2+3, self.y0+self.r2+3, outline=self.orange_color, extent=-20, style=ARC, width=8, start=180)
      
      self.setSpeed(0)
      self.setRPM(0)

   def setSpeed(self, value):
      self.speed = float(value)
      self.numberOfDataPoints += 1
      self.totalSpeed += self.speed
      self.meanSpeed = self.totalSpeed / self.numberOfDataPoints

      phi = self.speed_start_angle + self.speed_angle_range/self.max_number*value
      if phi>self.speed_start_angle + self.speed_angle_range-1.5*pi/180:
         phi = self.speed_start_angle + self.speed_angle_range-1.5*pi/180
      elif phi < self.speed_start_angle:
         phi = self.speed_start_angle
      x1 = self.x0 + (self.r1+1) * sin(phi)
      y1 = self.y0 - (self.r1+1) * cos(phi)
      x2 = self.x0 + (self.r6+3) * sin(phi)
      y2 = self.y0 - (self.r6+3) * cos(phi)
      self.canvas.delete(self.speedArrow) 
      self.canvas.delete(self.speedLabel)   
      self.canvas.delete(self.speedArc)                              
      self.speedLabel = self.canvas.create_text(self.x0, self.y0-(2*self.r1/3), font=('times', 38, 'bold'), fill=self.orange_color, text=str('%.0f' % self.speed))
      self.speedArrow = self.canvas.create_line(x1, y1, x2, y2, fill=self.orange_color, width=4)
      self.speedArc = self.canvas.create_arc(self.x0-self.r2-3, self.y0-self.r2-3, self.x0+self.r2+3, self.y0+self.r2+3, outline=self.orange_color, extent=(-self.speed_start_angle+phi)*(180/pi), style=ARC, width=8, start=90-(phi*180/pi))

   def setRPM(self, rpm):

      phi = self.speed_angle_range - self.speed_angle_range/5500*rpm
      x1 = self.x0 + (self.r1+1) * sin(phi)
      y1 = self.y0 - (self.r1+1) * cos(phi)
      x2 = self.x0 + (self.r6+3) * sin(phi)
      y2 = self.y0 - (self.r6+3) * cos(phi)
      self.canvas.delete(self.rpmArrow)   
      self.canvas.delete(self.rpmArc)                              
      self.rpmArrow = self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=4)
      self.rpmArc = self.canvas.create_arc(self.x0-self.r2-3, self.y0-self.r2-3, self.x0+self.r2+3, self.y0+self.r2+3, outline="blue", extent=-(self.speed_start_angle+phi)*(180/pi), style=ARC, width=8, start=90-self.speed_angle_range*180/pi)

   

   def reset(self):
      self.meanSpeed = 0
      self.numberOfDataPoints = 0
      self.totalSpeed = 0
      self.setSpeed(0)



# main
if __name__ =='__main__':

   def checkSerial(speed):
      var = raw_input("Command: " )
      if var == "s":
         value = raw_input("Speed: " )
         speed.setSpeed(float(value))
      elif var == "r":
         value = raw_input("RPM: " )
         speed.setRPM(float(value))

      root.after(1, checkSerial(speed))


   root = Tk()  
   c = SpeedometerGUI(300, 40, 4) 
   c.pack() 
   root.after(1, checkSerial(c))
   root.mainloop()