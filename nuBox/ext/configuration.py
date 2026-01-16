from pathlib import Path
from dynaconf import FlaskDynaconf

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


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


def load_extensions(app):
    extensions = app.config.get("EXTENSIONS")

    if not extensions:
        app.logger.warning("No EXTENSIONS configured")
        return

    if isinstance(extensions, str):
        import json
        extensions = json.loads(extensions)

    for extension in extensions:
        module_name, attr_name = extension.split(":")
        module = __import__(module_name, fromlist=[attr_name])
        ext = getattr(module, attr_name)

        if hasattr(ext, "init_app"):
            ext.init_app(app)
        elif callable(ext):
            ext(app)
        else:
            raise TypeError(
                f"Extension {extension} is neither callable nor has init_app()"
            )
