from flask import Blueprint, render_template, jsonify
from models.User import User as UserModel

users = Blueprint('users', __name__)


@users.route('/users')
def Users():
    return render_template()


@users.route('/api/users', methods=['GET'])
def get_users():
    result = UserModel.get_all_users()
    users_collection = []
    for user in result:
        users.append(user.__dict__)
    return jsonify(users=users_collection)


@users.route('/api/users/user/<id>', methods=['GET'])
def get_user(id):
    user = UserModel.get_user(id)
    return jsonify(user=user.__dict__)

