import os
import sys
import time
from gps import *

print 'Attempting to access GPS time...'

try:
	gpsd = gps(mode=WATCH_ENABLE)
except:
	print 'No GPS connection present. TIME NOT SET.'
	sys.exit()

while True:
	gpsd.next()
	if gpsd.utc != None and gpsd.utc != '':
		gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + str(int(gpsd.utc[11:12])+2) + gpsd.utc[13:19]
		print 'Setting system time to GPS time...'
	        print 'sudo date --set="%s"' % gpstime
		os.system('sudo date --set="%s"' % gpstime)
		print 'System time set.'
		sys.exit()
	time.sleep(1)
