from projetoFlask.ext.database import User
from flask import Blueprint
from flask_login import LoginManager

from .views import *

bpAuth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

bpAuth.add_url_rule('/login', view_func=login)
bpAuth.add_url_rule('/login', view_func=login_post, methods=['POST'])
bpAuth.add_url_rule('/signup', view_func=signup)
bpAuth.add_url_rule('/signup', view_func=signup_post, methods=['POST'])
bpAuth.add_url_rule('/logout', view_func=logout)

def init_app(app):
    app.register_blueprint(bpAuth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))