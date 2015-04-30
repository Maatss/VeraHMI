import os.path, time
while True:
	if os.path.exists("/dev/ttyUSB0"):
		print("0 found")
	elif os.path.exists("/dev/ttyUSB1"):
		print("1 found")
	else:
		print("Not found")

	time.sleep(1)