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

@users.route('/users/approval')
def get_user_approval():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))

    result = UserModel.get_user_approval()
    if result != 0:
        users = []
        for user in result:
            userItem = {}
            userItem['id'] = user.get_id()
            userItem['email'] = user.get_email()
            userItem['first_name'] = user.get_first_name()
            userItem['last_name'] = user.get_last_name()
            userItem['department'] = user.get_department_code()
            userItem['privileges'] = user.get_user_level()
            users.append(userItem)
    return render_template('acceptUsers.html', users=users)