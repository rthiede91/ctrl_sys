import socket, threading
import os
import MFRC522
import signal
import time


reading = True
MIFAREReader = MFRC522.MFRC522()

class register(threading.Thread):

	def __init__(self, connection):
		threading.Thread.__init__(self)
		self.connection = connection

	def run(self):
		cmd = 'y'
        	while cmd == 'y':
			nome = raw_input("Nome: ")
			rg = raw_input("RG: ")
			cpf = raw_input("CPF: ")
			entrada = raw_input("Hora de Entrada ")
			saida = raw_input("Hora de Saida ")

			print "Passe Cartao RFID:"
			card = False
			while card == False:
				(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                		if status == MIFAREReader.MI_OK:
                    			(status,uid) = MIFAREReader.MFRC522_Anticoll()
		    			rfid = str(uid[0])+'.'+str(uid[1])+'.'+str(uid[2])+'.'+str(uid[3])
                			self.connection.sendall("register;%s;%s;%s;%s;%s;%s" % (nome, rg, cpf, entrada, saida, rfid))
                			card = True
			time.sleep(1)
			
			cmd = raw_input("Continua? (y/n)  ")
		self.close()
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
					self.connection.send("identify;register")
					registerThread = register(self.connection)
					registerThread .start()
		
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

