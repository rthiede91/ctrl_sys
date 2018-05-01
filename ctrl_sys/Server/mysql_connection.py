import mysql.connector
import mysql_conf as msqlConf

def connect():
    
        usuario = "
        senha = "bvt"
        servidor = "127.0.0.1"
        banco = "acesso"

        try:
            conn = mysql.connector.connect(
                host=msqlConf.host, database=msqlConf.database, user=msqlConf.user, password=msqlConf.passwd,
                charset="utf8", use_unicode=True)

            msqlConn = self.conn.cursor()

            return msqlConn

        except mysql.connector.Error as err:
            print (err)