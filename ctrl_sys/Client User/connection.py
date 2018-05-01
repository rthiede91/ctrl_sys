import socket, threading
import os
import pyA20.gpio as GPIO
import MFRC522
import signal
import time
from pyA20.gpio import gpio
from pyA20.gpio import port


gpio.init()
gpio.setcfg(port.PG7, gpio.OUTPUT)
gpio.output(port.PG7, gpio.LOW)
time.sleep(2)
gpio.output(port.PG7, gpio.HIGH)
time.sleep(2)
gpio.output(port.PG7, gpio.LOW)	

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()


class readrfid(threading.Thread):

	def __init__(self, connection):

		threading.Thread.__init__(self)
		self.connection = connection

	def run(self):
		while True:
			while continue_reading:
    				(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    				if status == MIFAREReader.MI_OK:
    
    					(status,uid) = MIFAREReader.MFRC522_Anticoll()

					self.connection.sendall("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
					gpio.output(port.PG7, gpio.HIGH)
					time.sleep(2)
					gpio.output(port.PG7, gpio.LOW)



class ConnectionThread(threading.Thread):

	def __init__(self, connection):

		threading.Thread.__init__(self)
		self.connection = connection

	def run(self):
		while True:
			try:
				datas = self.connection.recv(1024)
				print("From Server: ", datas)

				if datas == "bye" or datas == '':
					self.connection.close()
					break

				if datas == "check":
					self.connection.sendall("0")
					readrfidThread = readrfid(self.connection)
					readrfidThread .start()

				if ";" in datas:
					data = datas.split(";")
					
					if data[0] == 'run':
						os.system(data[1])

			except Exception, msg:
				print ("OPA ", msg)
				break
				self.connection.close()


def sendMsg(self, msg):
	self.connection.sendall(bytes(msg))


serverAddr = "10.0.1.229"
port = 8080
filePort = 8081

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((serverAddr, port))

newThread = ConnectionThread(server)
newThread.start()

while True:
	out_data = raw_input("msg: ")
	server.sendall(bytes(out_data))
	if out_data=='bye':
		break

server.close()
