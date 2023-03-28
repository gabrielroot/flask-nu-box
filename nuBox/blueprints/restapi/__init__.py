from flask import Blueprint
from flask_restful import Api
from .resources.userResources import UsersResource, UserItemResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(UsersResource, "/users/")
api.add_resource(UserItemResource, "/user/<user_id>")


def init_app(app):
    app.register_blueprint(bp)
