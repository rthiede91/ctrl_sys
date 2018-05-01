import socket, threading, sys, time, eventos
from datetime import datetime

class ConnectionThread(threading.Thread):

    def __init__(self,clientAddress,clientsock):

        threading.Thread.__init__(self)
        
        self.csocket = clientsock
        self.clientAddress, self.clientPort = clientAddress
        
        print ("New Connection: ", clientAddress)
        
        self.csocket.send("identify")
        
    def run(self):

        while True:
            try:
                data = self.csocket.recv(1024)
                msg = data

                print ("From ",self.clientAddress,msg)
                
                if ";" in msg:
                    
                    data = msg.split(";")
                    
                    if data[0] == 'identify':
                        print(data[1])
                        self.csocket.send("check")
                    
                    if data[0] == 'register':
                        eventos.register(data[1],data[2],data[3],data[4],data[5],data[6])
                        self.csocket.send("Registrado")

                    if data[0] == 'rfid':
                        print('evento')
                        eventos.event(data[1])
                        for a in clientsUser:
                            print ("Client: ",a)
                            clientsUser[a].send("event;",data[1])
                            time.sleep(0.1)
                            print ("")
                        ## Inserir evento e LOG
                        ##CONSULTAR BANCO DE DADOS
                            #Resposta para PI
                            #Resposta para tela
                                                    
                if msg == '':
                    self.csocket.send(bytes("bye"))
                    print("Client at address ", self.clientAddress, " Disconnected")
                    self.csocket.close()
                    break
                        
                else:
                    print (" - ")
            
            except (Exception, err):
                print ("OPA  ", err)
                break


clientsCtrl={}
clientsUser={}
statusClient={}

def check_ctrl():
    # KEEP ALIVE
    print ("Checking")
    for a in theClient:
        print (a)
        clientsCtrl[a].send("keep")
        time.sleep(0.25)
        print ("")

def list_ctrl():
    #GIVE UP
    print ("Unidades de Controle")
    for a in theClient:
        print (a)
        clientsCtrl[a].send("give")
        time.sleep(0.25)
        print ("")

def list_user():
    #GIVE UP
    print ("Usuarios")
    for a in clientsUser:
        print (a)
        clientsUser[a].send("give")
        time.sleep(0.25)
        print ("")

def saytoclient(msg,ip):
    print("Send To ",ip," : ",msg)
    theClient[ip].send(msg)

def stop():
    print("Server Stoped")
    server.close()
    sys.exit(0)


def start_server_ctrl():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    localhost="10.0.1.229"
    port=8080
    server.bind((localhost, port))

    print("Server CTRL: Started")

    while True:
        try:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            clientsCtrl[clientAddress] = clientsock
            newThread = ConnectionThread(clientAddress, clientsock)
            newThread.start()

        except (Exception, err):
            print (err)

def start_server_user():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    localhost="10.0.1.229"
    port=8081
    server.bind((localhost, port))
    
    print("Server User: Started")
    
    while True:
        try:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            clientsUser[clientAddress] = clientsock
            newThread = ConnectionThread(clientAddress, clientsock)
            newThread.start()
        
        except (Exception, msg):
            print (msg)

