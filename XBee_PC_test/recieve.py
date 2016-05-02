#!/usr/bin/env python

import serial, time

with serial.Serial('/dev/cu.usbserial-00001014', 9600, timeout=1) as ser:
	while True:
		print(ser.readline())
