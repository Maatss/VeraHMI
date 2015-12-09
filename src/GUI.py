#!/usr/bin/env python
import pygame, os, sys
from math import *
import numpy



class GUI:
    def __init__(self, environment=None):
        if sys.platform == "linux2":
            "Ininitializes a new pygame screen using the framebuffer"
            # Based on "Python GUI in Linux frame buffer"
            # http://www.karoltomala.com/blog/?p=679
            disp_no = os.getenv("DISPLAY")
            if disp_no:
                print "I'm running under X display = {0}".format(disp_no)
            
            # Check which frame buffer drivers are available
            # Start with fbcon since directfb hangs with composite output
            drivers = ['fbcon', 'directfb', 'svgalib']
            found = False
            for driver in drivers:
                # Make sure that SDL_VIDEODRIVER is set
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                except pygame.error:
                    print 'Driver: {0} failed.'.format(driver)
                    continue
                found = True
                break
        
            if not found:
                raise Exception('No suitable video driver found!')

            self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        else:    
            pygame.display.init()
            self.size = (640,480)

        
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.done           = False

        fontPath            = "../Fonts/gotham.ttf"
        self.bigFont        = pygame.font.Font(fontPath, 70)
        self.mediumFont     = pygame.font.Font(fontPath, 40)
        self.smallFont      = pygame.font.Font(fontPath, 25)
        self.gpsEcuFont     = pygame.font.Font(fontPath, 40)
        self.clock          = pygame.time.Clock()
        self.environment    = environment

        # Define range of speedometer and rpm display
        self.maxSpeed  = 45
        self.maxRPM    = 5500 

        # Define colors
        self.orangeColor    = (250, 145, 33)
        self.blueColor      = (103, 255, 254) 
        self.greenColor     = (40, 255, 0)
        self.redColor       = (255, 40, 0)  

        # Define line widths
        self.smallLineWidth  = 4
        self.mediumLineWidth = 5
        self.largeLineWidth  = 8
        self.largerLineWidth = 16

        self.x0 = self.size[0]/2
        self.y0 = self.size[1]/2

        self.radius = min(self.x0, self.y0) * 0.9


        # Render the screen
        pygame.display.update()
        

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def drawBackground(self):
        # Draw speed and rpm meters
        rpmLoop = self.maxRPM/100
        self.drawLineInCirle(rpmLoop, 10, False, self.blueColor)
        self.drawLineInCirle(self.maxSpeed, 1, True, self.orangeColor)
        self.drawLineBetweenSpeedAndRPM()
        


    def drawLineBetweenSpeedAndRPM(self):
        y1 = self.y0 - (self.radius - 32)
        y2 = self.y0 - (self.radius + self.largerLineWidth)

        pygame.draw.line(self.screen, (255, 255, 255),(self.x0, y1), (self.x0, y2), self.mediumLineWidth)


    def drawLineInCirle(self, maxValue, deliminator, speedOrRPM, color):
        for i in range(0,maxValue+1):
            if speedOrRPM:
                phi = 21*pi/16 - (13*pi/16)/maxValue * i
            else:
                phi = -5*pi/16 + (13*pi/16)/maxValue * i

            x2 = self.x0 + self.radius * cos(phi)
            y2 = self.y0 - self.radius * sin(phi)

            if i == 0:
                x1 = self.x0 + (self.radius - 25) * cos(phi)
                y1 = self.y0 - (self.radius - 25) * sin(phi)
                x2 = self.x0 + (self.radius + self.largerLineWidth) * cos(phi)
                y2 = self.y0 - (self.radius + self.largerLineWidth) * sin(phi)
                pygame.draw.line(self.screen, (255, 255, 255),(x1, y1), (x2, y2), self.mediumLineWidth)

            # One lable every 10:th value and no label at zero
            elif i%10 == 0 and i != 0:    
                x1 = self.x0 + (self.radius - 25) * cos(phi)
                y1 = self.y0 - (self.radius - 25) * sin(phi)
                x  = self.x0 + (self.radius - 52) * cos(phi)
                y  = self.y0 - (self.radius - 52) * sin(phi)
                label = self.mediumFont.render(str(i/deliminator), 1, (255,255,255))
                self.screen.blit(label, (x-self.mediumFont.size(str(i/deliminator))[0]/2, y-self.mediumFont.size(str(i/deliminator))[1]/2))
                pygame.draw.line(self.screen, color,(x1, y1), (x2, y2), self.smallLineWidth)

            elif i%5 == 0 and i != maxValue:
                x1 = self.x0 + (self.radius - 22) * cos(phi)
                y1 = self.y0 - (self.radius - 22) * sin(phi)
                pygame.draw.line(self.screen, color,(x1, y1), (x2, y2), self.smallLineWidth)

            elif i != maxValue:
                x1 = self.x0 + (self.radius - 15) * cos(phi)
                y1 = self.y0 - (self.radius - 15) * sin(phi)
                pygame.draw.line(self.screen, color,(x1, y1), (x2, y2), self.smallLineWidth)


    def drawECUandGPS(self):
        if self.environment.ecuConnected:
            ecuColor = self.greenColor
        else: 
            ecuColor = self.redColor

        if self.environment.gpsConnected:
            gpsColor = self.greenColor
        else:
            gpsColor = self.redColor

        label = self.gpsEcuFont.render(str("GPS"), 1, gpsColor)
        self.screen.blit(label, (self.x0-self.gpsEcuFont.size("GPS")[0], self.y0+self.radius*0.97-self.gpsEcuFont.size("GPS")[1]))
        
        label = self.gpsEcuFont.render(str("ECU"), 1, ecuColor)
        self.screen.blit(label, (self.x0, self.y0+self.radius*0.97-self.gpsEcuFont.size("ECU")[1]))    


    def drawSpeedLabel(self):
        speed = str(int(round(self.environment.speed)))
        label = self.bigFont.render(speed, 1, (255, 255, 255))
        self.screen.blit(label, (self.x0 - self.bigFont.size(speed)[0]/2, self.y0-self.radius*0.75 + self.bigFont.size(speed)[1]/2)) 
        label = self.smallFont.render("km/h", 1, (255, 255, 255))
        self.screen.blit(label, (self.x0 - self.smallFont.size("km/h")[0]/2, self.y0 - self.radius*0.75 + self.bigFont.size(speed)[1] + self.smallFont.size("km/h")[1] + 5)) 

    def drawDashedLine(self, surf, color, start_pos, end_pos, width=1, dash_length=10):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = dash_length

        if (x1 == x2):
            ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
            xcoords = [x1] * len(ycoords)
        elif (y1 == y2):
            xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
            ycoords = [y1] * len(xcoords)
        else:
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = round(sqrt(a**2 + b**2))
            dx = dl * a / c
            dy = dl * b / c

            xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
            ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

        next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
        last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
        for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
            start = (round(x1), round(y1))
            end = (round(x2), round(y2))
            pygame.draw.line(surf, color, start, end, width)


    def drawArc(self, speedOrRPM, maxValue):
        if speedOrRPM:
            if self.environment.speed > maxValue:
                speed = maxValue-1
            elif self.environment.speed < 0:
                speed = 0
            else:
                speed = self.environment.speed

            phi         = 21*pi/16 - (13*pi/16)/maxValue * speed
            color       = self.orangeColor
            startAngle  = 21*pi/16

            # Draw mean speed
            if self.environment.meanSpeed > maxValue:
                meanSpeed = maxValue-1
            elif self.environment.meanSpeed < 0:
                meanSpeed = 0
            else:
                meanSpeed = self.environment.meanSpeed

            meanPhi = 21*pi/16 - (13*pi/16)/maxValue * meanSpeed
            x1      = self.x0 + (self.radius - 80) * cos(meanPhi)
            y1      = self.y0 - (self.radius - 80) * sin(meanPhi)
            x2      = self.x0 + (self.radius + self.largerLineWidth) * cos(meanPhi)
            y2      = self.y0 - (self.radius + self.largerLineWidth) * sin(meanPhi)
            self.drawDashedLine(self.screen, (255,255,0),(x1, y1), (x2, y2), self.mediumLineWidth, 5)


        else:
            if self.environment.rpm != None:
                if self.environment.rpm > maxValue:
                    rpm = maxValue-100
                elif self.environment.rpm < 0:
                    rpm = 0
                else:
                    rpm = self.environment.rpm
            else:
                rpm = 0

            phi         = -5*pi/16 + (13*pi/16)/maxValue * rpm
            color       = self.blueColor
            startAngle  = -5*pi/16


        # Draw line
        x1 = self.x0 + (self.radius - 80) * cos(phi)
        y1 = self.y0 - (self.radius - 80) * sin(phi)
        x2 = self.x0 + (self.radius + self.largerLineWidth) * cos(phi)
        y2 = self.y0 - (self.radius + self.largerLineWidth) * sin(phi)
        pygame.draw.line(self.screen, color,(x1, y1), (x2, y2), self.mediumLineWidth)

        # Draw arc
        if speedOrRPM:
            pygame.draw.arc(self.screen, color, (self.x0-self.radius-self.largerLineWidth, self.y0-self.radius-self.largerLineWidth, (self.radius+self.largerLineWidth)*2, (self.radius+self.largerLineWidth)*2), phi, startAngle, self.largerLineWidth)
        else:
            pygame.draw.arc(self.screen, color, (self.x0-self.radius-self.largerLineWidth, self.y0-self.radius-self.largerLineWidth, (self.radius+self.largerLineWidth)*2, (self.radius+self.largerLineWidth)*2), startAngle, phi, self.largerLineWidth)
       


    def drawTimers(self):
        #x = self.x0
        #y = self.y0
        #s = self.environment.totalTimeString
        #label = self.bigFont.render(s, 1, (255,255,255))
        #self.screen.blit(label, (self.x0-self.bigFont.size(s)[0]/2, self.y0-self.bigFont.size(s)[1]/2))
        label = self.bigFont.render(":", 1, (255,255,255))
        self.screen.blit(label, (self.x0 - self.bigFont.size(":")[0]/2, self.y0-self.bigFont.size(":")[1]/2))
        if self.environment.totalTime[0]<10:
            s = "0" + str(self.environment.totalTime[0])
        else:
            s = str(self.environment.totalTime[0])

        label = self.bigFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (self.x0-self.bigFont.size(s)[0]-5, self.y0-self.bigFont.size(s)[1]/2))

        if self.environment.totalTime[1]<10:
            s = "0" + str(self.environment.totalTime[1])
        else:
            s = str(self.environment.totalTime[1])

        label = self.bigFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (self.x0+5, self.y0-self.bigFont.size(s)[1]/2))


        # Current lap time
        label = self.mediumFont.render(":", 1, (255,255,255))
        self.screen.blit(label, (self.x0 - self.mediumFont.size(":")[0]/2, self.y0+self.bigFont.size(":")[1]/2 + 4))
        if self.environment.currentLapTime[0]<10:
            s = "0" + str(self.environment.currentLapTime[0])
        else:
            s = str(self.environment.currentLapTime[0])

        label = self.mediumFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (self.x0-self.mediumFont.size(s)[0]-5, self.y0+self.bigFont.size("00:00")[1]/2 + 4))

        if self.environment.currentLapTime[1]<10:
            s = "0" + str(self.environment.currentLapTime[1])
        else:
            s = str(self.environment.currentLapTime[1])

        label = self.mediumFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (self.x0+5, self.y0+self.bigFont.size("00:00")[1]/2 + 4))



#        x = self.x0
 #       y = self.y0+self.bigFont.size("00:00")[1]+3
  #      s = self.environment.lapTimeString
   #     label = self.mediumFont.render(s, 1, (255,255,255))
    #    self.screen.blit(label, (x-self.mediumFont.size(s)[0]/2, y-self.mediumFont.size(s)[1]/2))


               

    def drawLap(self):
        x = self.x0*1.9
        y = self.y0*0.1
        s = str(self.environment.currentLapNumber)
        label = self.bigFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (x-self.bigFont.size(s)[0], y))

        x = self.x0*1.9 - self.bigFont.size(s)[0] - self.smallFont.size("Lap")[0]*1.2
        y = self.y0*0.1
        s = str(self.environment.currentLapNumber)
        label = self.smallFont.render("Lap", 1, (255,255,255))
        self.screen.blit(label, (x, y))



    def drawTemperatures(self):

        x = self.x0*0.05
        y = self.y0*0.05
        if self.environment.topplockTemp != None:
            s = str(self.environment.topplockTemp)
        else:
            s = "--"
        label = self.mediumFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (x, y))

        x = self.x0*0.05
        y = self.y0*0.25
        if self.environment.topplockTemp != None:
            s = str(self.environment.cylinderTemp)
        else:
            s = "--"
        label = self.mediumFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (x, y))

        x = self.x0*0.05
        y = self.y0*0.45
        if self.environment.topplockTemp != None:
            s = str(self.environment.motorblockTemp)
        else:
            s = "--"
        label = self.mediumFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (x, y))

        x = self.x0*0.05 + self.mediumFont.size("00")[0]
        y = self.y0*0.05
        s = u'\N{DEGREE SIGN}' + "C"
        label = self.bigFont.render(s, 1, (255,255,255))
        self.screen.blit(label, (x, y))


    def drawInternetStatus(self):
        if self.environment.connectedTointernet:
            color = self.greenColor
        else:
            color = self.redColor

        s = "3G/4G"
        label = self.mediumFont.render(s, 1, color)
        self.screen.blit(label, (self.x0-self.mediumFont.size(s)[0]/2, self.y0+self.radius*0.78-self.mediumFont.size(s)[1]))


    def start(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            # Make entire screen black
            self.screen.fill((0, 0, 0))
            
            self.drawBackground()
            self.drawECUandGPS()
            self.drawSpeedLabel()
            self.drawArc(True, self.maxSpeed)
            self.drawArc(False, self.maxRPM)
            self.drawTimers()
            self.drawLap()
            self.drawTemperatures()
            self.drawInternetStatus()

            # Update display
            pygame.display.flip()
            self.clock.tick(10) # 


if __name__ == '__main__':
    class Environment:
        def __init__(self):
            self.speed=23
            self.rpm=1000
            self.totalTime = (12, 32)
            self.ecuConnected = True
            self.gpsConnected = True
            self.meanSpeed = 12
            self.currentLapNumber = 2
            self.currentLapTime = (3, 31)
            self.topplockTemp = 23
            self.cylinderTemp = 25
            self.motorblockTemp = 26
            self.connectedTointernet = False

    try:
        environment = Environment()
        gui = GUI(environment)
        gui.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        btn._Thread__stop()
        sys.exit()






