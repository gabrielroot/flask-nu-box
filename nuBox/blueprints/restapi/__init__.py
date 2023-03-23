from flask import Blueprint
from flask_restful import Api
from .resources import ProductResource, ProductItemResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(ProductResource, "/user/")
api.add_resource(ProductItemResource, "/user/<user_id>")

def init_app(app):
    app.register_blueprint(bp)