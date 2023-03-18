from flask import Blueprint
from .views import *

bp = Blueprint("webui", __name__, template_folder="templates",
    url_prefix="/", static_folder='static', static_url_path='/static/webui'
)

bp.add_url_rule('/', view_func=index)
bp.add_url_rule('/my-boxes', view_func=myBoxes)
bp.add_url_rule('/profile', view_func=profile)