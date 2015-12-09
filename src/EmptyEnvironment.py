#!/usr/bin/env python
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

      #### ECUHandler function
      def sendEcuVariables(self, values, connected):
            self.cylinderTemp       = values[0]
            self.topplockTemp       = values[1]
            self.motorblockTemp     = values[2]
            self.battyVoltage       = values[3]
            self.airPressure        = values[4]
            self.airTemperture      = values[5]
            self.rpm                = values[6]
            self.fuelMass           = values[7]
            self.ecuErrorCode       = values[8]

            #print(values)
            self.ecuConnected       = connected

