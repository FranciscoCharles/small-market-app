from flask import Flask
from application.ext import configuration

def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app

def create_app(**config):
    app = minimal_app(**config)
    return app