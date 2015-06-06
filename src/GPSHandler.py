#!/usr/bin/env python

import gps, threading, time, sys
 
class GPSHandler(threading.Thread):
	def __init__(self, gui = None, debug = False):
		threading.Thread.__init__(self)
		self.gui = gui

		#Initialize GPS 
		self.session = gps.gps("localhost", "2947")
		self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

		#Make the thread die with its parent
		self.deamon = True

		#Array to save GPS values in
		self.GPSValues = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

		#the names of all the data you can collect from the GPS (far from all is used right now)
		self.attributeNames = {'time': 0, 'lon': 1, 'lat': 2, 'alt': 3, 'climb': 4, 'speed': 5, 'device': 6, 'mode': 7, 'ept': 8, 'epx': 9, 'epy': 10, 'epv': 11, 'track': 12, 'epd': 13, 'eps': 14, 'epc': 15}
		self.unavailableCount = 0

		#Send message that GPS thread started
		if gui != None:
			self.gui.setGPS(self)
			self.gui.setStatus(1, 1, "Started")


#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def run(self):
		while True:
			try:
				report = self.session.next()
				# Wait for a 'TPV' report and display the current time,
				# To see all report data, uncomment the line below
				#print report
				if report['class'] == 'TPV':
					self.gui.connectGPSNoLog()
					if self.gui and self.unavailableCount>=5:
						self.gui.connectGPS()
					self.unavailableCount = 0

					#itterate over all the data points in GPS module and save them in self.GPSValues if they exists
					for attr in self.attributeNames.keys():
						if hasattr(report, attr):
							self.GPSValues[self.attributeNames[attr]] = report[attr]
							#print("attr: " + attr + " number: " + str(self.attributeNames[attr]))
						else:
							self.GPSValues[self.attributeNames[attr]] = None
							#print("Can't find " + attr)

					#if self.gui != None and self.GPSValues[self.attributeNames['speed']] != None:
						#print(self.GPSValues[self.attributeNames['speed']])
						#self.gui.setSpeed(self.GPSValues[self.attributeNames['speed']])

				else:
					#GPS not connected, set all values to None
					for x in range(len(self.GPSValues)):
						self.GPSValues[x] = None

					time.sleep(1)
					self.unavailableCount +=1
					if self.unavailableCount >=5:
						if self.unavailableCount <6:
							if self.gui != None:
								self.gui.disconnectGPS()
							print("GPS disconnected")
							self.unavailableCount +=1
						
				time.sleep(0.1)

			except KeyError:
				pass
			except StopIteration:
				session = None
				print "GPSD has terminated"

	def getGPSAttr(self, value):
		return self.GPSValues[self.attributeNames[value]]

	def getGPSPos(self):
		return (self.getGPSAttr("lat"), self.getGPSAttr('lon'), self.getGPSAttr('speed'))




#######################################################################################
################################ If running as main ###################################
#######################################################################################

if __name__ == '__main__':
	try:
		gps = GPSHandler()
		gps.start()
		while True:
			(lat, lon, speed) = gps.getGPSPos()
			print(lat, lon, speed)
			time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
		gps._Thread__stop()
		sys.exit("\n\ntBye...")



