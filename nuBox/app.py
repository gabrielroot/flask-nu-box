from flask import Flask
from nuBox.ext.configuration import init_app, load_extensions


def minimal_app(**config):
    app = Flask(
        __name__,
        instance_path="/tmp/instance",
        instance_relative_config=True,
    )
    init_app(app, **config)
    return app


def create_app(env=None, **config):
    if env:
        config.update(ENV_FOR_DYNACONF=env)

    app = minimal_app(**config)
    load_extensions(app)
    return app
