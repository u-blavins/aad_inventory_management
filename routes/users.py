from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify
from utils import Database
from models.User import User as UserModel

users = Blueprint('users', __name__)

@users.route('/users')
def Users():
    return render_template()

@users.route('/api/users', methods=['GET'])
def get_users():
    result = UserModel.get_all_users()
    users = []
    for user in result:
        users.append(user.__dict__)
    return jsonify(users=users)

@users.route('/api/users/user/<id>', methods=['GET'])
def get_user(id):
    user = UserModel.get_user(id)
    return jsonify(user=user.__dict__)

