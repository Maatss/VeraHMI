import serial, time

port = serial.Serial("/dev/tty.usbserial-FTCAMXWD",timeout=2)
count = 1

while True:
  port.flush()
  port.write("Hej" + str(count))
  print("Hej" +  str(count) + " sent!")
  count = count+1
  print("recieved: \t" + port.readline())
