from flask import Blueprint, render_template, jsonify, session, request, flash, redirect, url_for
from models.User import User as UserModel
from models.TransactionInfo import TransactionInfo as TransactionInfoModel

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

@users.route('/user/account')
def user_account():
    data = {}
    if 'user_id' in session:
        user = UserModel.get_user(session['user_id'])
        data['email'] = user.get_email()
        data['f_name'] = user.get_first_name()
        data['l_name'] = user.get_last_name()
        data['dept_code'] = user.get_department_code()

        trans_info = TransactionInfoModel.get_user_transactions(session['user_id'])
        
    return render_template('userSettings.html', data=data, transactions=trans_info)

@users.route('/user/reset/<id>', methods=['POST'])
def reset_password(id):
    if request.method == 'POST':
        if 'user_id' in session:
            if session['user_id'] == id:
                password = request.form['password']
                info = UserModel.update_user_password(id, password)
                flash(info[0][0])
    return redirect(url_for('users.user_account'))
