import os
from importlib import import_module
from pathlib import Path

from dynaconf import FlaskDynaconf

# Obtém o diretório raiz do projeto (onde está settings.toml)
ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def load_extensions(app):
    extensions = app.config.get("EXTENSIONS", [])

    if not extensions:
        app.logger.warning("No EXTENSIONS configured")
        return

    if isinstance(extensions, str):
        import json
        extensions = json.loads(extensions)

    for extension in extensions:
        module_name, extension_name = extension.split(":")
        module = __import__(module_name, fromlist=[extension_name])
        ext = getattr(module, extension_name)
        ext.init_app(app)



def init_app(app, **config):
    FlaskDynaconf(
        app,
        root_path=ROOT_PATH,
        settings_files=["settings.toml"],
        load_dotenv=True,
        environments=True,
        env_switcher="ENV_FOR_DYNACONF",
        **config
    )
