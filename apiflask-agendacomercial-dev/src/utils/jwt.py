from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from flask_apispec.annotations import use_kwargs
from flask import request
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
ERROR_MESSAGE = "Este campo no debe ser vacío"

ERROR_MESSAGE = "This field cannot be blank."


class TokenJWTResponseSchema(Schema):
    message = fields.Str(default='Success')


class TokenJWTRequestSchema(Schema):
    username = fields.String(required=True, description="Usuario")
    password = fields.String(required=True, description="Password")


class TokenJWT(MethodResource, Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True, help=ERROR_MESSAGE)
    parser.add_argument('password', type=str,
                        required=True, help=ERROR_MESSAGE)

    @doc(description='Post Transaction.', tags=['TokenJWT'])
    @use_kwargs(TokenJWTRequestSchema, location=('json'))
    @marshal_with(TokenJWTResponseSchema)
    def post(self, **kwargs):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        try:
            if not credenciales_validas(username,password):#hashed_password != credentials[2]:
                return jsonify({"message": "Bad password"})  # , 401
        except Exception as e:
            print(e)
            return jsonify({"message": "unexpected error(ln46)"})  # , 401

        access_token = create_access_token(identity=username, additional_claims={
            "is_administrator": False})
        print(access_token)
        return jsonify(access_token=access_token)

def credenciales_validas(usuario,clave):
    return True