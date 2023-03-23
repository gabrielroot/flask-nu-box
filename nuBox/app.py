from flask import Flask

from nuBox.ext import configuration


def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app


def create_app(**config):
    # O flask reconhece o padrão
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app