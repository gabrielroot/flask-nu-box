import os
from importlib import import_module
from pathlib import Path

from dynaconf import FlaskDynaconf

# Obtém o diretório raiz do projeto (onde está settings.toml)
ROOT_PATH = Path(__file__).resolve().parent.parent.parent


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
        root_path=ROOT_PATH,
        settings_files=["settings.toml"],
        load_dotenv=True,
        **config
    )
