import socket, threading
import os
import MFRC522
import signal
import time
from pyA20.gpio import gpio
from pyA20.gpio import port

gpio.init()
gpio.setcfg(port.PG7, gpio.OUTPUT)
gpio.output(port.PG7, gpio.LOW)


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

				if datas == "bye" or datas == '':
					self.connection.close()
					break

                    		if datas == "identify":
                        		self.connection.sendall("identify;ctrl")

				if datas == "check":
					self.connection.sendall("0")
					readrfidThread = readrfid(self.connection)
					readrfidThread .start()
		
				if ";" in datas:
					data = datas.split(";")
					
                			if data[0] == 'opendoor':
						print ("Abri porta")
                        			##Ativa RELE 2 Fechadura.
                    
					if data[0] == 'run':
						os.system(data[1])

			except Exception, msg:
				print ("OPA ", msg)
				break

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
