 import mysql_connection as msqlConn

 def registrar_usuario(self, nome, rg, cpf, hora_entrada, hora_saida, rfid):
    
    self.msqlConn = msqlConn.connect()
    
    try:
        self.msqlConn.execute(""" INSERT INTO users (nome,cpf,rg,entrada,saida,rfid) VALUES ('{}','{}','{}','{}','{}','{}') """
                        .format(nome, rg, cpf, hora_entrada, hora_saida, rfid))

        msqlConn.commit()

        self.msqlConn.close()

    except mysql.connector.Error as err:
        print (err)

def registrar_evento(self, rfid_user):
    self.id_user = rfid_user
    self.date = datetime.date.today()
    self.time = datetime.datetime.now().strftime("%H:%M:%S")

    self.msqlConn = msqlConn.connect()

    try:
        self.msqlConn.execute("""SELECT * FROM events WHERE iduser='{}' AND date='{}'  
            ORDER BY idevents DESC LIMIT 1"""
                    .format(self.id_user, self.date))

        row = msqlConn.fetchall()

        if not row or row[0][4] == 2:
            self.msqlConn.execute(""" INSERT INTO events VALUES ('', '{}', '{}', '{}', '{}') """
                        .format(self.id_user, self.date, self.time, 1))

            msqlConn.commit()

        else:
            self.msqlConn.execute(""" INSERT INTO events VALUES ('', '{}', '{}', '{}', '{}') """
                        .format(self.id_user, self.date, self.time, 2))
                        
            msqlConn.commit()

        msqlConn.close()

    #1 = entrada
    #2 = saida
    except mysql.connector.Error as err:
        print (err)