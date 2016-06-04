import serial, time

port = serial.Serial("/dev/tty.usbserial-FTWJCPQ3")
count = 1
port.flush()

while True:
  port.write("Hej" + str(count) + "\n")
  print("Hej" +  str(count) + " sent!")
  count = count+1
  print("recieved: \t" + port.readline())
  time.sleep(0.5)
