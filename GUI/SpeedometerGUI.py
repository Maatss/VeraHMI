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


      self.bgColor = "black"
      self.fgColor = "white"
      self.width = width
      self.height = self.width/2
      self.canvas = Canvas(self, width=self.width, height=self.height, highlightthickness=0, bg=self.bgColor)
      self.canvas.pack()

      self.x0 = self.width/2; lx = 9*self.width/20              # center and half-width of clock face
      self.y0 = self.height-11; ly = 18*self.height/20
      self.r0 = 0.77 * min(lx,ly)         # distance of labels from center     
      self.r1 = 0.60 * min(lx,ly)                     
      self.r2 = min(lx,ly)                          # length of arrow
      r3 = 0.95 * min(lx,ly)
      r4 = 0.90 * min(lx,ly)   
      r5 = 0.99 * min(lx,ly)

      self.canvas.create_oval(self.x0-lx, self.y0-ly, self.x0+lx, self.y0+ly, outline=self.fgColor, width=2)
      self.canvas.create_oval(self.x0-self.r1, self.y0-self.r1, self.x0+self.r1, self.y0+self.r1, outline=self.fgColor, width=1)

      for i in range(0,number_of_labels+1):
         phi = -pi/2 + pi/number_of_labels * i
         x = self.x0 + self.r0 * sin(phi)
         y = self.y0 - self.r0 * cos(phi)
         self.canvas.create_text(x, y, fill=self.fgColor, font=('times', 22, 'bold'), text=str(max_number/number_of_labels*i))

      for i in range(0,max_number+1):
         phi = -pi/2 + pi/max_number * i
         if i%(max_number/number_of_labels) != 0:
            x1 = self.x0 + r3 * sin(phi)
            y1 = self.y0 - r3 * cos(phi)
         else:
            x1 = self.x0 + r4 * sin(phi)
            y1 = self.y0 - r4 * cos(phi)

         x2 = self.x0 + r5 * sin(phi)
         y2 = self.y0 - r5 * cos(phi)
         self.canvas.create_line(x1, y1, x2, y2, fill=self.orange_color, width=2)

      y = self.y0-(self.height/8)
      self.canvas.create_rectangle(self.x0-30, y-16, self.x0+30, y+16, outline=self.fgColor)

      self.mean = self.canvas.create_text(self.x0, self.y0-(self.height/3), fill="red", font=('times', 30, 'bold'), text="0")
      self.arrow = self.canvas.create_line(self.x0, self.y0, x, y, arrow=LAST, fill=self.orange_color, width=5)  
      self.arc = self.canvas.create_arc(self.x0-self.r2, self.y0-self.r2, self.x0+self.r2, self.y0+self.r2, outline=self.orange_color, extent=180, style=ARC, width=5, start=180)
      self.setSpeed(0)

   def setSpeed(self, value):
      self.speed = float(value)
      self.numberOfDataPoints += 1
      self.totalSpeed += self.speed
      self.meanSpeed = self.totalSpeed / self.numberOfDataPoints

      phi = -pi/2 + pi/50*value
      x1 = self.x0 + self.r1 * sin(phi)
      y1 = self.y0 - self.r1 * cos(phi)
      x2 = self.x0 + self.r2 * sin(phi)
      y2 = self.y0 - self.r2 * cos(phi)
      self.canvas.delete(self.arrow) 
      self.canvas.delete(self.mean)   
      self.canvas.delete(self.arc)                              
      self.mean = self.canvas.create_text(self.x0, self.y0-(self.height/8), font=('times', 30, 'bold'), fill=self.fgColor, text=str('%.0f' % self.meanSpeed))
      self.arrow = self.canvas.create_line(x1, y1, x2, y2,  arrow=LAST, fill=self.orange_color, width=5)
      self.arc = self.canvas.create_arc(self.x0-self.r2, self.y0-self.r2, self.x0+self.r2, self.y0+self.r2, outline=self.orange_color, extent=20, style=ARC, width=5, start=180-(phi*180/pi))

   def reset(self):
      self.meanSpeed = 0
      self.numberOfDataPoints = 0
      self.totalSpeed = 0
      self.setSpeed(0)

# main
if __name__ =='__main__':
   root = Tk()  
   c = SpeedometerGUI(300, 40, 8) 
   c.pack() 
   root.mainloop()