from logging import exception
import os
import cx_Oracle

from utils.config_source.dot_properties_adapter import dot_properties_adapter
#ports
class iauth_db:
    def validar_usuario(username:str) -> list:
        raise Exception(" iauth_db is an interface...")

    def hash_pwd(password:str) -> str:
        raise Exception(" iauth_db is an interface...")

#adapters
class oracle_auth_db(iauth_db):
    def validar_usuario(username:str):
        cfg:dot_properties_adapter = dot_properties_adapter()
        connection = cx_Oracle.connect(
            user=cfg.get_property('datasource.nueve.usr'), password=cfg.get_property('datasource.nueve.pwd'), dsn=cfg.get_property('datasource.nueve.dns'), encoding="UTF-8")
        cur = connection.cursor()
        query = "select ID, CLIENT, SECRET from wscore.wts_users where upper(client) = upper(:client)"
        print(query)
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            credentials = row
        else:
            credentials = None
        connection.close()
        return credentials

    def hash_pwd(password:str):
        cfg:dot_properties_adapter = dot_properties_adapter()
        connection = cx_Oracle.connect(
            user=cfg.get_property('datasource.nueve.usr'), password=cfg.get_property('datasource.nueve.pwd'), dsn=cfg.get_property('datasource.nueve.dns'), encoding="UTF-8")
        cur = connection.cursor()
        hashed_password = cur.callfunc('wscore.hash_password.encrypt', str, [password])
        connection.close()
        return hashed_password

# class fake_auth_db(iauth_db):
#     def validar_usuario(username:str):
#         return ['69','faker','1bdb6ca805f9a721f0dd38745be45f524d063b47dd1b441cc72ca672ed82ee11']

#     def hash_pwd(password:str):
#         return "1bdb6ca805f9a721f0dd38745be45f524d063b47dd1b441cc72ca672ed82ee11"