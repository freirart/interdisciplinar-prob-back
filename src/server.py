from flask import Flask
from flask_cors import CORS

from api.naive_bayes import setup_blueprint as naive_bayes_blueprint


app = Flask(__name__)
CORS(app)

def register_blueprint(app):
	app.register_blueprint(naive_bayes_blueprint())


def run_server():
	port = 5000

	register_blueprint(app)

	print("> Starting app")
	app.run(host="0.0.0.0", threaded=False, port=port)
