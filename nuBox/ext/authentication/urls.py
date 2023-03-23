from flask import Blueprint

from .views import *

bpAuth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

bpAuth.add_url_rule('/login', view_func=login)
bpAuth.add_url_rule('/login', view_func=login_post, methods=['POST'])
bpAuth.add_url_rule('/signup', view_func=signup)
bpAuth.add_url_rule('/signup', view_func=signup_post, methods=['POST'])
bpAuth.add_url_rule('/logout', view_func=logout)