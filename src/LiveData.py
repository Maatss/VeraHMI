#!/usr/bin/env python

import time, datetime, random, math, threading, os, serial

class LiveData(threading.Thread):
    def __init__(self, environment):
        threading.Thread.__init__(self)
        self.daemon = True
        self.environment = environment

        self.port = serial.Serial('/dev/ttyUSB0', 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3.0)
        self.connectedToTeam = True


    def run(self):
        while True:
            if self.environment != None:
                if self.environment.timerRunning:
                    data = self.environment.ecuDataArray
                    self.sendECUValues(data  + [self.environment.speed] + [self.environment.gpsPos[0],self.environment.gpsPos[1]])
            time.sleep(1)

        
    def sendECUValues(self, logs):
        now = datetime.datetime.now()
        date = "%s-%s-%s" % (now.year, now.month, now.day)
        logs = logs + [date, now.hour, now.minute, now.second, now.microsecond]
        stringToSend = "#BASE:"
        for log in logs:
            stringToSend += "%s+" % str(log)
        # Remove last plus sign from string and add new line 
        stringToSend = stringToSend[:-1] + "&\n"
        self.port.write(stringToSend)


    def sendSpeed(self, speed):
        pass

###########################################################################
# If run as main
#

if __name__ == '__main__':
    live = LiveData()
    live.start()
    while True:
        sensor_data1 = math.sin(time.time())*10 + 10
        sensor_data2 = -random.random()*10

        temp1 = math.cos(time.time()/10)*5 + 3
        temp2 = 4
        temp3 = math.cos(time.time()*2)*3 - 2

        air_temp = math.sin(time.time()*10) + random.random() + 20 - math.cos(time.time())/5
        air_pressure = math.sin(time.time()*9) + random.random() + 1000 - math.cos(time.time())/6
        logs = [sensor_data1, sensor_data2, temp1, temp2, temp3, air_temp, air_pressure]
        #print logs
        live.sendECUValues(logs)

        speed = random.random()*50
        live.sendSpeed(speed)

        time.sleep(0.5) # delay between stream posts










