#!/usr/bin/env python
import pygame, os
from math import *



class GUI:
    def __init__(self, environment=None):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['directfb', 'fbcon', 'svgalib']
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
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.done           = False

        fontPath            = "/home/pi/VeraHMI/Fonts/gotham.ttf"
        self.bigFont        = pygame.font.Font(fontPath, 70)
        self.mediumFont     = pygame.font.Font(fontPath, 40)
        self.smallFont      = pygame.font.Font(fontPath, 20)
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
        self.screen.blit(label, (self.x0-4-self.gpsEcuFont.size("GPS")[0], self.y0+self.radius*0.85-self.gpsEcuFont.size("GPS")[1]))
        
        label = self.gpsEcuFont.render(str("ECU"), 1, ecuColor)
        self.screen.blit(label, (self.x0+4, self.y0+self.radius*0.85-self.gpsEcuFont.size("ECU")[1]))    


    def drawSpeedLabel(self):
        speed = str(int(round(self.environment.speed)))
        label = self.bigFont.render(speed, 1, (255, 255, 255))
        self.screen.blit(label, (self.x0 - self.bigFont.size(speed)[0]/2, self.y0-self.radius*0.75 + self.bigFont.size(speed)[1]/2)) 
        label = self.smallFont.render("km/h", 1, (255, 255, 255))
        self.screen.blit(label, (self.x0 - self.smallFont.size("km/h")[0]/2, self.y0 - self.radius*0.75 + self.bigFont.size(speed)[1] + self.smallFont.size("km/h")[1] + 5)) 


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

            # Update display
            pygame.display.flip()
            self.clock.tick(10) # 








