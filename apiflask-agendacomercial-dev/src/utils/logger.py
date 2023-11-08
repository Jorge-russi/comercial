import os
import cx_Oracle
class Logger:
    @classmethod
    def logger(cls, usuario, ip, body, resp, message, cod_resp, cod_internal):
        connection = cx_Oracle.connect(user=os.environ["ORA_USER"], password=os.environ["ORA_PASSWORD"], dsn=os.environ["ORA_DSN"], encoding="UTF-8")
        cursor = connection.cursor()
        inssql = "INSERT INTO WSCORE.WTS_LOG_RESP (ID, USUARIO, IP, CUERPO, RESPUESTA, MENSAJE, COD_RESPUESTA, COD_INTERNO ) VALUES ( WTS_LOG_RESP_SEQ.NEXTVAL, :USUARIO, :IP, :CUERPO, :RESPUESTA, :MENSAJE, :COD_RESPUESTA, :COD_INTERNO)"
        cursor.execute(inssql , (usuario, ip, body, resp, message, cod_resp, cod_internal))
        connection.commit()