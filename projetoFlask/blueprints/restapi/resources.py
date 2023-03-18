from flask import jsonify, abort
from flask_restful import Resource
from projetoFlask.ext.database import User

class ProductResource(Resource):
    def get(self):
        users = User.query.all() or abort(204)
        return jsonify(
            {'products': [
                user.to_dict()
                for user in users
            ]}
        )

class ProductItemResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first() or abort(
            404
        )
        return jsonify(user.to_dict())