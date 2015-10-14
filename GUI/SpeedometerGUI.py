#!/usr/bin/env python

from Tkinter import *
from math import *

class SpeedometerGUI(Frame):

   def __init__(self, width, max_number, number_of_labels):
      Frame.__init__(self)
      self.bgColor = "black"
      self.fgColor = "white"
      height = width/2
      self.canvas = Canvas(self, width=width, height=height, highlightthickness=0, bg=self.bgColor)
      self.canvas.pack()

      self.x0 = width/2; lx = 9*width/20              # center and half-width of clock face
      self.y0 = height-10; ly = 18*height/20
      self.r0 = 0.82 * min(lx,ly)         # distance of labels from center                             # length of hour hand
      self.r2 = 0.95 * min(lx,ly)                          # length of arrow
      r3 = 0.95 * min(lx,ly)
      r4 = 0.90 * min(lx,ly)   
      r5 = 0.99 * min(lx,ly)

      self.canvas.create_oval(self.x0-lx, self.y0-ly, self.x0+lx, self.y0+ly, outline=self.fgColor, width=2)
      for i in range(0,number_of_labels+1):
         phi = -pi/2 + pi/number_of_labels * i
         x = self.x0 + self.r0 * sin(phi)
         y = self.y0 - self.r0 * cos(phi)
         self.canvas.create_text(x, y, fill=self.fgColor, text=str(max_number/number_of_labels*i))  

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
         self.canvas.create_line(x1, y1, x2, y2, fill="red", width=1)

      self.arrow = self.canvas.create_line(self.x0, self.y0, x, y, arrow=LAST, fill="orange", width=3)  
      self.setSpeed(0)

   def setSpeed(self, value):
      phi = -pi/2 + pi/50*value
      x = self.x0 + self.r2 * sin(phi)  
      y = self.y0 - self.r2 * cos(phi)
      self.canvas.delete(self.arrow)                               
      self.arrow = self.canvas.create_line(self.x0, self.y0, x, y, arrow=LAST, fill="orange", width=3)

   def reset(self):
      self.setSpeed(0)

# main
if __name__ =='__main__':
   root = Tk()  
   c = SpeedometerGUI(300, 150, 40, 8) 
   c.pack() 
   root.mainloop()