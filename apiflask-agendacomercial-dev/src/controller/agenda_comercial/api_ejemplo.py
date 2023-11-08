import os,json
import traceback
import cx_Oracle
from flask import jsonify
from flask_restful import Resource, reqparse
from utils.utils import del_null_fields

from utils.repositorio.v1.adaptadores_orcl.test_sisafi import test_sisafi_adapter,repositorio_orcl

#Swagger
from marshmallow import Schema, fields
from flask_apispec import marshal_with, doc, use_kwargs, MethodResource
from flask_jwt_extended import jwt_required, get_jwt_identity

ERROR_MESSAGE = "This field cannot be blank."

class ApiEjemploResponseSchema(Schema):
    message = fields.Str(default='Success')
class ApiEjemploRequestSchema(Schema):
    atributo1 = fields.String(required=True, description="Descripcion del atributo1")
    atributo2 = fields.Boolean(required=True, description="Descripcion del atributo2")
    atributo3 = fields.Integer(required=True, description="Descripcion del atributo3")
    atributo_opcional = fields.String(required=False, description="Descripcion del atributo opcional")

class ApiEjemplo(MethodResource, Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('atributo1', type=str, required=True, help=ERROR_MESSAGE)
    parser.add_argument('atributo2', type=bool, required=True, help=ERROR_MESSAGE)
    parser.add_argument('atributo3', type=int, required=True, help=ERROR_MESSAGE)
    parser.add_argument('atributo_opcional', type=str, required=False, help=ERROR_MESSAGE)

    @doc(description='Actualizacion de datos de un afiliado.', tags=['ApiEjemplo'], responses={
        200: {"description": "Description of status 200..."},
        401: {"description":'Description of error 401...'}
    })
    @use_kwargs(ApiEjemploRequestSchema, location=('json'))
    @marshal_with(ApiEjemploResponseSchema)
    @jwt_required()#define  que debe tener un tokenvalido para poderejecutarse
    def post(self, **kwargs):
        requestData = ApiEjemplo.parser.parse_args()
        headers = {'Content-Type': 'application/json'}

        current_user = get_jwt_identity()
        usuarios_autorizados = ["user"]
        if current_user not in usuarios_autorizados:
            response = {
                "status":400,
                "message":"el usuario del WS no tiene permisos para ejecutar este metodo"
            }
            return jsonify( {"respuesta":response} )
    
        try:
            del_null_fields(requestData)
            response = ejecutar_logica_del_negocio(requestData)
            return jsonify({"respuesta":response})
        except Exception as e:
            response = str(e)
            traceback.print_exc()
            
        
        

def ejecutar_logica_del_negocio(data_json) -> list:
    db:repositorio_orcl = test_sisafi_adapter()
    
    #ejemplo 1: select
    query:str = """
        select :atributo1
        from dual
    """
    parametros:dict = {
        "atributo1" : data_json["atributo1"]
    }
    respuesta = db.ejecutar_query(query,parametros)
    
    #ejemplo 2: ejecutar funcion
    funcion:str = "sysmemp.alguna_funcion"
    parametros:dict = [
        data_json["atributo1"]
    ]
    respuesta = db.ejecutar_funcion(funcion,parametros,int)
    
    #ejemplo 3: ejecutar funcion que retorna un cursor
    funcion:str = "sysmemp.alguna_funcion"
    parametros:dict = [
        data_json["atributo1"]
    ]
    respuesta = db.ejecutar_funcion(funcion,parametros,retorna_cursor=True)
    
    #ejemplo 4: ejecutar procedimiento
    procedimiento:str = "sysmemp.algun_procedimiento"
    parametros_salida:dict = [
        "atributo1",
        "atributo2"
    ]
    orden_parametros={
        "nombre_parametro":"tipo_de_dato"
    }
    respuesta = db.ejecutar_procedimiento_con_parametros(procedimiento,orden_parametros,data_json,parametros_salida)
    
    return {"response_code":200}
    