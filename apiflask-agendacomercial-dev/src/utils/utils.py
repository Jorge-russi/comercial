from flask import jsonify, make_response
from datetime import datetime, timedelta
from utils.config_source.dot_properties_adapter import dot_properties_adapter
from utils.repositorio.v1.repositorio_orcl import repositorio_orcl

def del_null_fields(json:dict) -> dict:
    """elimina los campos que son nulos en un diccionario

    Args:
        json (dict): diccionario y objeto equivalente
         que requiera eliminar valores de claves nulas

    Returns:
        dict_debuged: diccionario sin los campos nulos.
    """
    for key in dict(json):
        if json[key] is None:
            json.pop(key)
    return json

def send_response(object_to_jsonify, status_code:int = 200):
    return make_response(jsonify(object_to_jsonify), status_code)

def parse_unix_2_datetime(fecha_en_unix:int) -> datetime:

    if len(str(fecha_en_unix)) >= 12:
        fecha_en_unix = fecha_en_unix / 1000
    
    fecha_datetime = datetime.fromtimestamp(fecha_en_unix)
    return fecha_datetime

def parse_unix_2_dateint(fecha_en_unix:int) -> int:
    fecha_datetime = parse_unix_2_datetime(fecha_en_unix)
    fecha_dateint = int(fecha_datetime.strftime('%Y%m%d'))
    return fecha_dateint

def parse_str_2_bool(valor:str) -> bool:
    if valor.upper() == 'TRUE':
        return True
    else:
        return False