from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to recieve")

while 1:
	connectionSocket, addr = serverSocket.accept()
	message, clientAddress = connectionSocket.recv(2048)
	modifiedMessage = message.upper()
	connectionSocket.send(modifiedMessage)
	print("message \"" + modifiedMessage + "\" sent to " + clientAddress[0])

connectionSocket.close