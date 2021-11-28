import flask_restful as restful
from flask import request
from flask_restful import reqparse

from models import NaiveBayes

class NaiveBayesRoutes(restful.Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("nomes")
        args = parser.parse_args()

        nb = NaiveBayes()

        return {
            "message": "Success get on Naive Bayes Routes!",
            "analysis": nb.get_analysis_table()
        }
