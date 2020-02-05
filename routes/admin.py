from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

from models.Item import Item as ItemModel
from  models.User import User as UserModel

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def Admin():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('admin.html')
    return redirect(url_for('auth.Auth'))

@admin.route('/admin/transactions')
def transactions():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('generateReport.html')
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/purchase-order')
def purchase_order():
    if 'privilege' in session:
        if session['privilege'] == 3:
            return redirect(url_for('admin.Admin'))
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/stock')
def stocks():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            items = ItemModel.get_all_items()
            return render_template('viewStock.html', items=items)
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/add-stock')
def add_stock():
    if 'privilege' in session:
        if session['privilege'] == 3:
            return render_template('addItemToInventory.html')
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/return')
def return_items():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('returnItems.html')
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/accept-users')
def accept_users():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
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
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/accept/<id>', methods=['POST'])
def accept(id):
    if request.method == 'POST':
        query = """
                    UPDATE
                        [StoreManagement].[usr].[User]
                    SET
                        [isApproved] = 1
                    WHERE
                        [ID] = '%s'
                """ % id
        Database.execute(query)
    return redirect(url_for('admin.accept_users'))

@admin.route('/admin/deny/<id>', methods=['POST'])
def deny(id):
    if request.method == 'POST':
        query = """
                        DELETE FROM
                            [StoreManagement].[usr].[User]
                        WHERE
                            [ID] = '%s'
                    """ % id
        Database.execute(query)
    return redirect(url_for('admin.accept_users'))