import os
from importlib import import_module

from dynaconf import FlaskDynaconf

# Obtém o diretório raiz do projeto (onde está settings.toml)
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_extensions(app):
    for extension in app.config.EXTENSIONS:
        # Split data in form `extension.path:factory_function`
        module_name, factory = extension.split(":")
        # Dynamically import extension module.
        ext = import_module(module_name)
        # Invoke factory passing app.
        getattr(ext, factory)(app)


def init_app(app, **config):
    FlaskDynaconf(
        app,
        settings_files=[os.path.join(ROOT_PATH, "settings.toml")],
        **config
    )
