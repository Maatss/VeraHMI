#!/usr/bin/env python

import serial, time

count = 0
with serial.Serial('/dev/cu.usbserial-00002014', 9600, timeout=1) as ser:
	ser.flush()
	while True:
		ser.write("Hello world: "+str(count) + "\n")

		print(ser.readline())

		count += 1
		time.sleep(1)