from flask import Blueprint
from flask_restful import Api

from .naive_bayes import NaiveBayesRoutes

def setup_blueprint():
    blueprint = Blueprint(
        "naive_bayes_routes", __name__
    )

    api = Api(blueprint)
    api.add_resource(NaiveBayesRoutes, "/naive_bayes")

    return blueprint
