#!/usr/bin/env python

import time, datetime, random, math, threading, thread, os

class LiveData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        while True:
            time.sleep(1)

        




###########################################################################
# Update values
#
    def sendECUValues(self, logs):
        if self.readyForData:
            pass



    def sendSpeed(self, speed):
        if self.readyForData:
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










