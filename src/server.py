import os
from flask import Flask
from flask_cors import CORS

from api.naive_bayes import setup_blueprint as naive_bayes_blueprint


app = Flask(__name__)
app.register_blueprint(naive_bayes_blueprint())
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
