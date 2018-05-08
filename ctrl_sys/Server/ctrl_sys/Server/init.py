import socket, threading, sys, time, eventos
from datetime import datetime
import base64

import blob

class ConnectionUserThread(threading.Thread):

    def __init__(self,clientAddress,clientsock):

        threading.Thread.__init__(self)
        
        self.csocket = clientsock
        self.clientAddress, self.clientPort = clientAddress
        
        print ("New Connection: ", clientAddress)
        
        self.csocket.send("identify\n")
        
    def run(self):

        while True:
            try:
                data = self.csocket.recv(1024)
                msg = data

                print ("From ",self.clientAddress,msg)
                
                if ";" in msg:
                    
                    data = msg.split(";")
                    

                    if data[0] == 'identify':
                        self.csocket.send("check\n")
                    
                if msg == '':
                    clientsUser[clientAddress] = "off"
                    print("Client at address ", self.clientAddress, " Disconnected")
                    self.csocket.close()
                    break
                        
                else:
                    print (" - ")
            
            except Exception, err:
                print ("OPA  ", err)
                break

class ConnectionCtrlThread(threading.Thread):

    def __init__(self,clientAddress,clientsock):

        threading.Thread.__init__(self)
        
        self.csocket = clientsock
        self.clientAddress, self.clientPort = clientAddress
        self.cid = str(self.clientAddress)+":"+str(self.clientPort)
        clientsCtrl[self.cid] = clientsock

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

                    if data[0] == 'door':
                        if data[1] == "0":
                            if statusCtrl[self.cid] == "openDoor":
                                statusCtrl[self.cid] = "doorIsOpen"
                                print("porta primaria aberta")
                                print("Aguardar Fechamento")

                            elif statusCtrl[self.cid] == "openDoorSec":
                                statusCtrl[self.cid] = "doorIsOpenSec"
                                print("porta secundaria abertia")
                                print("Aguardar Fechamento")

                            else:
                                print("Anomalia - Porta Aberta")
                                statusCtrl[self.cid] = "doorIsOpen"
                                update_users("alert"," ("+identifyCtrl[self.cid]+") Porta Aberta")

                        if data[1] == "1":
                            if statusCtrl[self.cid] == "doorIsOpen":
                                statusCtrl[self.cid] = "doorIsClosed"
                                print("porta primaria fechada")
                                print("enviar comando para abrir porta secundaria")
                        
                                if identifyCtrl[self.cid] == "orctrl01":
                                    print("abrir porta orctrl02")
                                    clientsCtrl[identifyCtrl["orctrl02"]].send("openDoor")
                                    statusCtrl[identifyCtrl["orctrl02"]] = "openDoorSec"

                                if identifyCtrl[self.cid] == "orctrl02":
                                    print("abrir porta orctrl01")
                                    clientsCtrl[identifyCtrl["orctrl01"]].send("openDoor")
                                    statusCtrl[identifyCtrl["orctrl01"]] = "openDoorSec"

                            elif statusCtrl[self.cid] == "doorIsOpenSec":
                                statusCtrl[self.cid] = "doorIsClosed"
                                print("porta secundaria Fechado")
                                print("FIM")
                            
                            else:
                                print("Anomalia - Porta Fechada!!!")
                                statusCtrl[self.cid] = "doorIsClosed"
                                update_users("alert"," ("+identifyCtrl[self.cid]+") Porta Fechada")

                    if data[0] == 'identify':
                        print(data[1])
                        
                        identifyCtrl[self.cid] = data[1]
                        identifyCtrl[data[1]] = self.cid

                        statusCtrl[self.cid] = "doorIsClosed"
                        
                        self.csocket.send("check")
                        self.csocket.send("checkDoor")
                        self.csocket.send("rfid")
                    
                    if data[0] == 'register':
                        eventos.register(data[1],data[2],data[3],data[4],data[5],data[6])
                        self.csocket.send("Registrado")

                    if data[0] == 'rfid':
                        print('evento')
                        eventos.event(data[1])
                        if identifyCtrl[self.cid] == "orctrl01":
                            if statusCtrl[self.cid] == "doorIsClosed":
                                if statusCtrl[identifyCtrl["orctrl02"]] == "doorIsClosed":
                                    self.csocket.send("openDoor")
                                    statusCtrl[self.cid] = "openDoor"
                                    update_users("eventAccess",data[1])
                                else:
                                    update_users("alert","Acesso Negado(orctrl01): Porta orctrl02 Aberta")
                            else:
                                update_users("alert","Acesso Negado(orctrl01): Porta orctrl01 Aberta")
                        if identifyCtrl[self.cid] == "orctrl02":
                            if statusCtrl[self.cid] == "doorIsClosed":
                                if statusCtrl[identifyCtrl["orctrl01"]] == "doorIsClosed":
                                    self.csocket.send("openDoor")
                                    statusCtrl[self.cid] = "openDoor"
                                    update_users("eventAccess",data[1])
                                else:
                                    update_users("alert","Acesso Negado(orctrl02): Porta orctrl01 Aberta")
                            else:
                                update_users("alert","Acesso Negado(orctrl02): Porta orctrl02 Aberta")
                                    

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
            
            except Exception, err:
                print ("OPA  ", err)
                break


clientsCtrl={}
identifyCtrl={}
statusCtrl={}


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

def update_users(func, msg):
    if func == "eventAccess":
        for a in clientsUser:
            print (a)
            with open("pic.png", "rb") as image_file:
                blobStr = base64.b64encode(image_file.read())
                self.csocket.send("startImage\n")
                self.csocket.send(str(blobStr))
                self.csocket.send("\n")
                self.csocket.send("endImage\n")
                self.csocket.send("\n")
                name="nome=Roberto Thiede;"
                rg="rg=21.917.671-6;"
                cpf="cpf=045.485.141-39;"
                entrada="entrada=8:00;"
                saida="saida=18:00"
                self.csocket.send("event;"+name+rg+cpf+entrada+saida+"\n")
                self.csocket.send("check\n")
            time.sleep(0.25)
            print ("")

    if func == "alert":
        for a in clientsUser:
            if clientsUser[a] != "off":
                clientsUser[a].send(func+";"+msg+"\n")

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
            newThread = ConnectionCtrlThread(clientAddress, clientsock)
            newThread.start()

        except Exception, msg:
            print (msg)

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
            newThread = ConnectionUserThread(clientAddress, clientsock)
            newThread.start()
        
        except Exception, msg:
            print (msg)

