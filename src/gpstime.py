#!/usr/bin/env python

import os, sys, time
from gps import *

def setTImeFromGPS(hoursOfUTC):
	print 'Attempting to access GPS time...'

	try:
		gpsd = gps(mode=WATCH_ENABLE)
	except:
		print 'No GPS connection present. TIME NOT SET.'
		sys.exit()

	while True:
		gpsd.next()
		if gpsd.utc != None and gpsd.utc != '':
			hours = str(int(gpsd.utc[11:13]) + hoursOfUTC)
			gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + hours + gpsd.utc[13:19]
			print 'Setting system time to GPS time...'
			os.system('sudo date --set="%s"' % gpstime)
			print 'System time set.'
			sys.exit()
		time.sleep(1)

if __name__ == '__main__':
	setTImeFromGPS(2)

