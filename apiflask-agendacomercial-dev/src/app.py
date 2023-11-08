'''
    Document the file.
'''
import os, datetime
import logging
import logging.handlers
from flask_restful import Api
from datetime import timedelta
from flask import Flask, jsonify, session
from flask_wtf import CSRFProtect 
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from utils.jwt import TokenJWT

from controller.agenda_comercial.api_ejemplo import ApiEjemplo

import cx_Oracle

load_dotenv()  # invoca variables de entorno

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "alguna clave secreta"
app.config["PROPAGATE_EXCEPTIONS"] = True
jwt = JWTManager(app)

api = Api(app)

spec = APISpec(title='Api Agenda Comercial',
               version='v1',
               plugins=[MarshmallowPlugin()],
               openapi_version='3.0.0')
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("jwt", jwt_scheme)

app.config.update({
    'APISPEC_SPEC': spec,
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
})


docs = FlaskApiSpec(app)

#rutas api
api.add_resource(ApiEjemplo,"/api/agenda/v1/ejemplo")

# API
## Token Generator
api.add_resource(TokenJWT, '/api/agenda/v1/auth/token')


# Registrar cada clase en swagger
docs.register(TokenJWT)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(message="Token Has Expired"), 412

# HOST & PORT
if __name__ == "__main__":
    from waitress import serve
    handler = logging.handlers.RotatingFileHandler(
        'app.log',
        maxBytes=1024 * 1024)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('This message goes to stderr and app.log!')
    app.run(port=5000)
