from flask import jsonify, abort
from flask_restful import Resource
from nuBox.ext.database import User as UserModel
from nuBox.blueprints.restapi.schema.UserSchema import UserSchema


class UsersResource(Resource):
    schema = UserSchema()

    def get(self):
        users = UserModel.query.all() or abort(204)
        return jsonify(self.schema.dump(users, many=True))


class UserItemResource(Resource):
    schema = UserSchema()

    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first() or abort(404)
        return jsonify(self.schema.dump(user))
