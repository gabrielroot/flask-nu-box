from nuBox.ext.database import User
from flask_login import LoginManager

from .urls import bpAuth


def init_app(app):
    app.register_blueprint(bpAuth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
