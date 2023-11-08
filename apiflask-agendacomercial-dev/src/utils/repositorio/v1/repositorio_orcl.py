import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine,text
import json
from utils.config_source.dot_properties_adapter import dot_properties_adapter
class repositorio_orcl:
    
    def __init__(self, dns:str, user:str, password:str ) -> None:
        self.user=user
        self.password=password
        self.dns=dns
        self.parametros_salida_pr = {}

    def __dar_formato_df_2_list(self, df:pd.DataFrame):
        result = df.to_json(orient="index")
        dict_parsed = json.loads(result)
        producto:list = []
        for i_registro in dict_parsed:
            registro = dict_parsed[i_registro]
            producto.append(registro)
        return producto

    def ejecutar_query(self, sql:str, parametros:dict=None) -> list:
        oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{dns}'

        engine = create_engine(
            oracle_connection_string.format(
                username=self.user,
                password=self.password,
                dns=self.dns
            )
        )

        #data as DataFrame
        data = pd.DataFrame(engine.connect().execute(text(sql), parametros))
        #data as dict
        data = self.__dar_formato_df_2_list(data)
        return data

    def ejecutar_funcion(self, nombre_funcion:str, parametros:list, tipo_de_dato_retorno=None, retorna_cursor:bool=False) -> list:
        conexion:cx_Oracle.Connection = cx_Oracle.connect(
            user=self.user, password= self.password, dsn=self.dns, encoding="UTF-8"
        )
        
        cursor:cx_Oracle.Cursor = conexion.cursor()
        if retorna_cursor and tipo_de_dato_retorno is None:
            cursor_retorno = cursor.var(cx_Oracle.CURSOR)
            cursor_retorno = cursor.callfunc(nombre_funcion, cx_Oracle.CURSOR, parametros)
            #data as cursor
            data = cursor_retorno.fetchall()
            if len(data) == 0:
                data = []
            else:
                #data as DataFrame
                data = pd.DataFrame(data, columns=[str.lower(i[0]) for i in cursor_retorno.description])
                #data as dict
                data = self.__dar_formato_df_2_list(data)
        else:
            data = cursor.callfunc(nombre_funcion, tipo_de_dato_retorno, parametros)
            data = [data]
        conexion.commit()
        cursor.close()
        conexion.close()
        del cursor
        del conexion
        return data
    
    def ejecutar_procedimiento(self, nombre_procedimiento:str, parametros:list) -> list:
        conexion:cx_Oracle.Connection = cx_Oracle.connect(
            user=self.user, password= self.password, dsn=self.dns, encoding="UTF-8"
        )
        
        cursor:cx_Oracle.Cursor = conexion.cursor()
        
        cursor.callproc(nombre_procedimiento, parametros)
        #data as cursor
        cursor.close()
        conexion.close()
        del cursor
        del conexion
    
    def ejecutar_procedimiento_con_parametros(self, nombre_procedimiento:str, ordenamiento_parametros:list, parametros_entrada:dict, parametros_salida:dict) -> dict:
        conexion:cx_Oracle.Connection = cx_Oracle.connect(
            user=self.user, password= self.password, dsn=self.dns, encoding="UTF-8"
        )
        
        cursor:cx_Oracle.Cursor = conexion.cursor()
        parametros = []
        self.parametros_salida_pr = parametros_salida
        for clave_parametro in ordenamiento_parametros:
            valor_parametro = parametros_entrada.get(clave_parametro)
            if valor_parametro is None:
                valor_parametro = parametros_salida.get(clave_parametro)
                if valor_parametro is None:
                    raise Exception("parametro "+valor_parametro+" no existe.")
                else:
                    self.__convertir_parametro_salida(clave_parametro, valor_parametro,  cursor)
                    parametros.append(parametros_salida[clave_parametro])
            else:
                parametros.append(valor_parametro)
            
                   
        cursor.callproc(nombre_procedimiento, parametros)
        self.__procesar_cursores()
        cursor.close()
        conexion.close()
        del cursor
        del conexion
        return self.parametros_salida_pr
        
        
    #TODO: migrate to real class
    def ejecutar_insert(self, sql:str, parametros:dict):

        oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{dns}'

        engine = create_engine(
            oracle_connection_string.format(
                username=self.user,
                password=self.password,
                dns=self.dns
            )
        )
        conexion = engine.connect()
        conexion.execute(text(sql), parametros).close()
        conexion.commit()
        conexion.close()

    def ejecutar_update(self, sql:str, parametros:dict):

        self.ejecutar_insert(sql, parametros)

    def __convertir_parametro_salida(self, nombre_parametro:str, tipo_dato:str, cursor:cx_Oracle.Cursor):
        if(tipo_dato == "CURSOR"):
            self.parametros_salida_pr[nombre_parametro] = cursor.var(cx_Oracle.CURSOR)
        elif(tipo_dato == "int"):
            parametro = cursor.var(cx_Oracle.int)
        else:
            pass
    
    def __procesar_cursores(self):
        for parametro in self.parametros_salida_pr.keys():
            cursor = self.parametros_salida_pr[parametro]
            if str(type(cursor))=="<class 'cx_Oracle.Var'>":
                lista_serializada = cursor.getvalue()
                encabezados = self.__obtener_homologacion_encabezados(lista_serializada.description)
                lista_serializada = pd.DataFrame(lista_serializada)
                lista_serializada = lista_serializada.rename(columns=encabezados)
                lista_serializada = self.__dar_formato_df_2_list(lista_serializada)
                self.parametros_salida_pr[parametro] = lista_serializada
    
    def __obtener_homologacion_encabezados(self,lista_encabezados:list) -> dict:
        homologaciones = {}
        for posicion_encabezado in range(len(lista_encabezados)):
            nombre = lista_encabezados[posicion_encabezado][0]
            homologaciones[posicion_encabezado] = nombre
        return homologaciones
            