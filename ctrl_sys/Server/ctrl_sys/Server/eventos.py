# -*-  coding: utf-8 -*-
import mysql.connector
import datetime
import sys

class Conexao(object):

    def __init__(self, usuario="", senha="", banco="", servidor=""):
        usuario = "bvt"
        senha = "bvt"
        servidor = "127.0.0.1"
        banco = "acesso"

        try:
            self.conecta = mysql.connector.connect(
                host=servidor, database=banco, user=usuario, password=senha,
                charset="utf8", use_unicode=True)
            c = self.conecta.cursor()
            c.close()
        except mysql.connector.Error as err:
            print err

class Eventos(object):

    def __init__(self, id_event="", id_user="", date="", time="", type_event=""):
        self.id_event = id_event
        self.id_user = id_user
        self.date = date
        self.time = time
        self.type_event = type_event

    def get_user(rfid):
    
        conexao = Conexao()
        c = conexao.conecta.cursor()
    
        try:
            c.execute(""" SELECT nome,cpf,rg,entrada,saida,foto from users WHERE rfid = '{}' """
                      .format(rfid))
            row = c.fetchall()
            print row[0][0]
        except mysql.connector.Error as err:
            print err

    def registrar_usuario(self, nome, rg, cpf, hora_entrada, hora_saida, rfid):

        conexao = Conexao()
        c = conexao.conecta.cursor()

        try:
            c.execute(""" INSERT INTO users (nome,cpf,rg,entrada,saida,rfid) VALUES ('{}','{}','{}','{}','{}','{}') """
                          .format(nome, rg, cpf, hora_entrada, hora_saida, rfid))
            conexao.conecta.commit()
            c.close()
        except mysql.connector.Error as err:
            print err

    def registrar_evento(self, rfid_user):
        self.id_user = rfid_user
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().strftime("%H:%M:%S")

        conexao = Conexao()
        c = conexao.conecta.cursor()

        try:
            c.execute("""SELECT * FROM events WHERE iduser='{}' AND date='{}'  
                
                ORDER BY idevents DESC LIMIT 1"""
                      .format(self.id_user, self.date))
            row = c.fetchall()
            if not row or row[0][4] == 2:
                c.execute(""" INSERT INTO events VALUES ('', '{}', '{}', '{}', '{}') """
                          .format(self.id_user, self.date, self.time, 1))
                conexao.conecta.commit()
            else:
                c.execute(""" INSERT INTO events VALUES ('', '{}', '{}', '{}', '{}') """
                          .format(self.id_user, self.date, self.time, 2))
                conexao.conecta.commit()
            c.close()
        #1 = entrada
        #2 = saida
        except mysql.connector.Error as err:
            print err

    def valida_user(self, rfid):
        conexao = Conexao()
        c = conexao.conecta.cursor()
        self.rfid_user = rfid

        try:
            c.execute(""" SELECT rfid FROM users where rfid='{}' """
                      .format(self.rfid_user))
            row = c.fetchall()
            if not row:
                print "usuario não encotrado"
            else:
                print "Evento registrado"
                self.registrar_evento(rfid)
        except mysql.connector.Error as err:
            print err


def register(nome, rg, cpf, hora_entrada, hora_saida, rfid):
	insert_event = Eventos()
	insert_event.registrar_usuario(nome, rg, cpf, hora_entrada, hora_saida, rfid)

def event(rfid):
	insert_event = Eventos()
	insert_event.valida_user(rfid)
