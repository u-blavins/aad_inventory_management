from flask import Blueprint, render_template, jsonify, session, request, flash, redirect, url_for
from models.User import User as UserModel
from models.TransactionInfo import TransactionInfo as TransactionInfoModel
from models.Transaction import Transaction as TransactionModel
users = Blueprint('users', __name__)


@users.route('/users')
def Users():
    return render_template()


@users.route('/api/users', methods=['GET'])
def get_users():
    if session['privilege'] in [2,3]:
        result = UserModel.get_all_users()
        users_collection = []
        for user in result:
            users.append(user.__dict__)
        return jsonify(users=users_collection)


@users.route('/api/users/user/<id>', methods=['GET'])
def get_user(id):
    if session['privilege'] in [2,3]:
        user = UserModel.get_user(id)
        return jsonify(user=user.__dict__)

@users.route('/user/account')
def user_account():
    data = {}
    if 'user_id' in session:
        user = UserModel.get_user(session['user_id'])

        data['id'] = user.get_id()
        data['email'] = user.get_email()
        data['f_name'] = user.get_first_name()
        data['l_name'] = user.get_last_name()
        data['dept_code'] = user.get_department_code()

        user_orders = TransactionModel.get_all_user_transactions(session['user_id'], 0)
        user_refunds = TransactionModel.get_all_user_transactions(session['user_id'], 1)
    return render_template('userSettings.html', data=data, orders=user_orders, refunds=user_refunds)


@users.route('/user/reset/<id>', methods=['POST'])
def reset_password(id):
    if request.method == 'POST':
        if 'user_id' in session:
            if session['user_id'] == id:
                password = request.form['password']
                if password == '':
                    flash('Password field cannot be empty')
                else:
                    info = UserModel.update_user_password(id, password)
                    flash(info[0][0])
    return redirect(url_for('users.user_account'))


@users.route('/<transaction_id>', methods=['GET'])
def department_transaction_info(transaction_id):
    if request.method == 'GET':
        if 'privilege' in session:
            transaction_info = TransactionInfoModel.get_transaction_info(transaction_id)
            transaction = TransactionModel.get_transaction(transaction_id)
            is_refund = transaction.get_refund()
            if is_refund is False:
                transaction_type = "order"
            else:
                transaction_type = "refund"
            return render_template('transactioninfo.html', transaction_info=transaction_info,
                                   transaction_id=transaction_id, type=transaction_type)
    return redirect(url_for('admin.Admin'))