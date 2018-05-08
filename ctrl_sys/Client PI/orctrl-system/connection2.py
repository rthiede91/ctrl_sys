import socket, threading
import os
import MFRC522
import signal
import time
from pyA20.gpio import gpio
from pyA20.gpio import port


doorPin=port.PG7
checkDoorPin=port.PG6

gpio.init()

gpio.setcfg(doorPin, gpio.OUTPUT)
gpio.setcfg(checkDoorPin, gpio.INPUT)

gpio.output(doorPin, gpio.LOW)

class checkDoor(threading.Thread):

	def __init__(self, connection):
		threading.Thread.__init__(self)
		self.connection = connection
		
	def run(self):
		self.connection.send("Check Door Iniciado")
		statusDoor = 0
            	while True:
			time.sleep(2)
			readDoorPin = gpio.input(doorPin)
			if(readDoorPin != statusDoor):
				statusDoor = readDoorPin
				print ("Door")
                    		self.connection.send("rfid;door")

class readrfid(threading.Thread):

	def __init__(self, connection):
		threading.Thread.__init__(self)
		self.connection = connection
		self.reading = True
		self.MIFAREReader = MFRC522.MFRC522()

	def run(self):
		self.connection.send("RFID Iniciado")
            	while self.reading:
                	(status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
                	if status == self.MIFAREReader.MI_OK:
				print ("card")
              			(status,uid) = self.MIFAREReader.MFRC522_Anticoll()
		
                    		self.connection.send("rfid;%s.%s.%s.%s" % (uid[0], uid[1], uid[2], uid[3]))
                    		time.sleep(1)


class ConnectionThread(threading.Thread):

	def __init__(self, connection):

		threading.Thread.__init__(self)
		self.connection = connection

	def run(self):
		while True:
			try:
				datas = self.connection.recv(1024)
                
				print("From server: ", datas)

				#Funcoes Simples
				if datas == "bye" or datas == '':
					self.connection.close()
					break

				if datas == "openDoor":
					openDoor()	

                    		if datas == "identify":
                        		self.connection.sendall("identify;orctrl02")

				if datas == "check":
					self.connection.sendall("0")

				if datas == "checkDoor":
					checkDoorThread = checkDoor(self.connection)
					#checkDoorThread.start()
				
				if datas == "rfid":
					readrfidThread = readrfid(self.connection)
					#readrfidThread.start()

				#Funcoes Complexas	
				if ";" in datas:
					data = datas.split(";")
                    
					if data[0] == 'run':
						os.system(data[1])

			except Exception, msg:
				print ("OPA ", msg)
				break

def openDoor():
	gpio.output(doorPin, gpio.HIGH)
	time.sleep (2)
	gpio.output(doorPin, gpio.LOW)

def sendMsg(self, msg):
	self.connection.sendall(bytes(msg))


serverAddr = "10.0.1.229"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((serverAddr, port))

newThread = ConnectionThread(server)
newThread.start()

while True:
	out_data = raw_input("msg: ")
	if out_data=='bye':
		break
	server.send(out_data)

server.close()
