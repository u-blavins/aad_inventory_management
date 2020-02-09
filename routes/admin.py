from flask import Blueprint, request, render_template, redirect, session, url_for
from utils.Database import Database

from models.Item import Item as ItemModel
from models.User import User as UserModel
from models.PurchaseOrder import PurchaseOrder as PurchaseOrderModel

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
            purchase_orders_pending = PurchaseOrderModel.get_purchase_orders_pending()
            pending = []
            for order in purchase_orders_pending:
                pending_order = {'purchase_order_id': order.get_purchase_order_id(),
                                 'generated_by': order.get_generated_by(),
                                 'generated_date': order.get_generated_date()}
                pending.append(pending_order)

            purchase_orders_history = PurchaseOrderModel.get_purchase_orders_history()
            history = []
            for order in purchase_orders_history:
                history_order = {'purchase_order_id': order.get_purchase_order_id(),
                                 'generated_by': order.get_generated_by(),
                                 'generated_date': order.get_generated_date(),
                                 'completion_date': order.get_completion_date()}
                history.append(history_order)

            return render_template('purchaseOrder.html', pending=pending,
                                   history=history)
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
                    user_item = \
                        {'id': user.get_id(), 'email': user.get_email(), 'first_name': user.get_first_name(),
                         'last_name': user.get_last_name(), 'department': user.get_department_code(),
                         'privileges': user.get_user_level()}
                    users.append(user_item)
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
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()
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
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()
    return redirect(url_for('admin.accept_users'))
