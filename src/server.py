import os
from flask import Flask
from flask_cors import CORS

from api.naive_bayes import setup_blueprint as naive_bayes_blueprint


app = Flask(__name__)
CORS(app)

def register_blueprint(app):
	app.register_blueprint(naive_bayes_blueprint())


def run_server():
	register_blueprint(app)
	app.run()
