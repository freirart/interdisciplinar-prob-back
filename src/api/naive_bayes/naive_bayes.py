import flask_restful as restful
from flask import request
from flask_restful import reqparse
from json import loads

from models import NaiveBayes

class NaiveBayesRoutes(restful.Resource):

    def get(self):
        nb = NaiveBayes()

        return { "info": nb.get_model_info() }
        
    def post(self):
        try:
            data = request.get_json()
        except Exception as e:
            data = loads(request.get_data().decode("ISO-8859-1"))
        
        if isinstance(data, dict) and "nomes" in data and isinstance(data["nomes"], list):
            nb = NaiveBayes()
            
            return { "names_by_gender": nb.names_by_gender(data["nomes"]) }
        
        return { "error": "O corpo da requisição deve conter a chave 'nomes' com uma lista." }, 400
