#!/usr/bin/env python

import threading, thread, time, serial, pynmea2, os, sys

 
class GPSHandler(threading.Thread):
	def __init__(self, environment=None):
		threading.Thread.__init__(self)
		self.daemon 		= True
		self.environment 	= environment	
		self.gpsPos		 	= (None, None)
		self.gpsSpeed 		= None
		self.timeSet	 	= False


		#Array to save GPS values in
		#self.GPSValues = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
		#the names of all the data you can collect from the GPS (far from all is used right now)
		#self.attributeNames 	= {'time': 0, 'lon': 1, 'lat': 2, 'alt': 3, 'climb': 4, 'speed': 5, 'device': 6, 'mode': 7, 'ept': 8, 'epx': 9, 'epy': 10, 'epv': 11, 'track': 12, 'epd': 13, 'eps': 14, 'epc': 15}
		

		try:
			os.system('stty -F /dev/ttyAMA0 raw 9600 cs8 clocal -cstopb')
			self.serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)		
		except:
			print("Could not connect to GPS, continuing...")
		


#######################################################################################
################################## Class functions ####################################
#######################################################################################


	def parseGPS(self, str):
	    if str.find('GGA') > 0:
	        msg = pynmea2.parse(str)
	        if len(msg.lat) > 2:
	        	self.environment.gpsConnected = True
	        	self.gpsPos = (msg.lat + msg.lat_dir, msg.lon + msg.lon_dir)
	        	# Set time according to GPS time
	        	if not self.timeSet:
	        		print 'Setting system time to GPS time...'
	        		gpsTime = "%s:%s:%s" % (msg.timestamp.hour, msg.timestamp.minute, msg.timestamp.second)
	        		if gpsTime != None:
	        			os.system('sudo date -u --set="%s"' % gpsTime)
	        			self.timeSet = True
	        			print 'System time set.'

	        else:
	        	self.gpsPos = (None, None)
	        	self.environment.gpsConnected  = False

	     	if self.environment != None:
	        	self.environment.gpsPos = self.gpsPos


	def reconnectToGPS(self):
		try:
			self.serialPort.close()
		except Exception as e:
			print(e)
		# Try to (re-)open the port
		try:
			self.serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)		
		except Exception as e:
			print("Could not connect to GPS, continuing...")
			print(e)



	def run(self):
		while True:
			try:
				str = self.serialPort.readline()
   				self.parseGPS(str)
   			except Exception as e:
   				print(e)
   				# Try to close port
   				self.environment.gpsConnected  = False
   				self.reconnectToGPS()
   				



#######################################################################################
################################## If run as main #####################################
#######################################################################################

if __name__ == '__main__':
	try:
		gps = GPSHandler()
		gps.start()
		while True:
			(lat, lon) = gps.gpsPos
			if gps.environment != None:
				print("Lat: " + str(lat) + ",    Long: " + str(lon) + "     Connected: " + str(gps.environment.gpsConnected))
			else:
				print("Lat: " + str(lat) + ",    Long: " + str(lon))
		
			time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
		gps._Thread__stop()
		sys.exit("\n\ntBye...")





    


