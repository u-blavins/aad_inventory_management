from flask import Blueprint, request, render_template, redirect, session, url_for, make_response, flash, jsonify
from io import StringIO
import csv

from utils.Database import Database
from utils.Email import Email

from models.Item import Item as ItemModel
from models.User import User as UserModel
from models.PurchaseOrder import PurchaseOrder as PurchaseOrderModel
from models.PurchaseOrderInfo import PurchaseOrderInfo as PurchaseOrderInfoModel
from models.ReturnItems import ReturnItems as ReturnItemsModel
from models.Billing import Billing as BillingModel
from models.Transaction import Transaction as TransactionModel
from models.TransactionInfo import TransactionInfo as TransactionInfoModel

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def Admin():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('admin.html')
    return redirect(url_for('auth.Auth'))


@admin.route('/admin/purchase-order')
def purchase_order():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
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


@admin.route('/admin/purchase-order/<order_id>', methods=['GET'])
def purchase_order_info(order_id):
    if request.method == 'GET':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                results = PurchaseOrderInfoModel.get_purchase_order_info(order_id)
                print(results)
                order_info = []
                for result in results:
                    info = {'item_code': result.get_item_code(), 'quantity': result.get_quantity(),
                            'is_complete': result.get_is_complete(), 'completion_date': result.get_completion_date(),
                            'approved_by': result.get_approved_by()}
                    order_info.append(info)
                return render_template('purchaseorderinfo.html', order_info=order_info, order_id=order_id)
    return redirect(url_for('admin.purchase_order'))


@admin.route('/admin/purchase-order/<order_id>/<item_code>', methods=['POST'])
def confirm_item_delivery(order_id, item_code):
    if request.method == 'POST':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                PurchaseOrderInfoModel.confirm_delivery(order_id, item_code, session['user_id'])
                return redirect(f'/admin/purchase-order/{order_id}')
    return redirect(url_for('admin.Admin'))


@admin.route('/admin/purchase-order/create', methods=['POST'])
def create_purchase_order():
    if request.method == 'POST':
        if 'privilege' in session:
            if session['privilege'] == 3:
                codes = request.form.getlist('codes[]')
                quantity = request.form.getlist('quantity[]')
                pairs = []
                if codes.__len__() == quantity.__len__():
                    count = codes.__len__()
                    for i in range(count):
                        pair = (codes[i], quantity[i])
                        pairs.append(pair)
                    conn = Database.connect()
                    cursor = conn.cursor()
                    order_id = PurchaseOrderModel.create_purchase_order(session['user_id'], cursor)
                    if order_id is not None:
                        for pair in pairs:
                            response = PurchaseOrderInfoModel.create_purchase_order_info(order_id, pair[0], pair[1],
                                                                                         cursor)
                            if response == 'Failure':
                                cursor.rollback()
                                conn.close()
                                return redirect(url_for('admin.purchase_order'))
                        cursor.commit()
                        conn.close()
                return redirect(url_for('admin.purchase_order'))
    return redirect(url_for('admin.Admin'))


@admin.route('/admin/purchase-order/download/<order_id>', methods=['GET'])
def download_purchase_order(order_id):
    get_order_info = PurchaseOrderInfoModel.get_purchase_order_info(order_id)
    order_info = [('ItemCodes', 'Quantity')]
    for info in get_order_info:
        order_info.append((info.get_item_code(), info.get_quantity()))
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(order_info)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={order_id}.csv"
    output.headers["Content-type"] = "text/csv"
    return output


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


@admin.route('/admin/returns')
def returns():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('returnItems.html')
    return redirect(url_for('admin.Admin'))


@admin.route('/api/returns/items', methods=['POST'])
def return_items():
    if request.method == 'POST':
        email = request.form['email']
        if email != '':
            user = UserModel.get_user_by('[Email]', email)
            if user != None:
                codes = request.form.getlist('codes[]')
                quantity = request.form.getlist('quantity[]')
                unit_types = request.form.getlist('unitTypes[]')
                option = request.form.getlist('returnOption[]')
                returns = ReturnItemsModel()
                msgs = []
                for i in range(len(codes)):
                    msg = returns.set_returns(codes[i].upper(), int(quantity[i]),
                                              unit_types[i], option[i])
                    if msg != '':
                        msgs.append(msg)
                        flash(msg)
                if len(msgs) == 0:
                    msg = returns.return_items(user.get_id(), session['user_id'])
                    flash(msg)
            else:
                flash('User does not exist')
        else:
            flash('Please enter an email address')
    return redirect(url_for('admin.returns'))


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


@admin.route('/admin/view-users')
def view_users():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            users = UserModel.get_all_users()
            if len(users) != 0:
                return render_template('users.html', users=users)
    return redirect(url_for('admin.Admin'))


@admin.route('/admin/update-privilege/<id>', methods=['POST'])
def update_user_privilege(id):
    if 'privilege' in session:
        privilege = int(request.form['privilege'])
        if session['privilege'] == 3:
            if privilege in [0, 1, 2, 3]:
                response = UserModel.update_user_privilege(id, privilege)
                flash(response)
            else:
                flash('Please select a privilege level to update to')
    return redirect(url_for('admin.view_users'))


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


@admin.route('/admin/billing')
def billing():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            results = BillingModel.get_billing_rows()
            if results != 0:
                billing_rows = []
                for row in results:
                    billing_row = {'month_name': BillingModel.get_billing_month_name(row.get_billing_month()),
                                   'billing_month': row.get_billing_month(), 'billing_year': row.get_billing_year()}
                    billing_rows.append(billing_row)
                return render_template('billing.html', billing_rows=billing_rows)
    return redirect(url_for('admin.Admin'))


@admin.route('/admin/billing/download/<year>/<month>', methods=['GET'])
def download_finance_report(year, month):
    if request.method == 'GET':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                results = BillingModel.get_department_billing(year, month)
                department_billing = [('Department', 'Total')]
                for row in results:
                    bill = (row.get_department_code(), row.get_total())
                    department_billing.append(bill)

                si = StringIO()
                cw = csv.writer(si)
                cw.writerows(department_billing)
                output = make_response(si.getvalue())
                output.headers["Content-Disposition"] = f"attachment; filename=FinanceReport-{year}-{month}.csv"
                output.headers["Content-type"] = "text/csv"
                return output
    return redirect(url_for('admin.billing'))


@admin.route('/admin/billing/info/<year>/<month>', methods=['GET'])
def billing_info(year, month):
    if request.method == 'GET':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                results = BillingModel.get_department_billing(year, month)
                billing_rows = []
                for row in results:
                    billing_row = {'department_code': row.get_department_code(), 'total': row.get_total()}
                    billing_rows.append(billing_row)
                return render_template('billinginfo.html', billing_rows=billing_rows,
                                       year=year, month=month,
                                       month_name=BillingModel.get_billing_month_name(int(month)))
    return redirect(url_for('admin.billing'))


@admin.route('/admin/billing/info/<year>/<month>/<department>', methods=['GET'])
def department_transaction(year, month, department):
    if request.method == 'GET':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                transaction_query = f"""
                    SELECT
                        [TransactionID],
                        [Email],
                        [DepartmentCode],
                        [Price],
                        [TransactionDate],
                        [isRefund]
                    FROM
                        [itm].[DepartmentTransactionsByYearMonth]('{department}',{month},{year},0)
                    ORDER BY
                        [TransactionDate] DESC, [Price] DESC
                        """
                department_transactions = TransactionModel.get_transaction_by(transaction_query)
                refund_query = f"""
                    SELECT
                        [TransactionID],
                        [Email],
                        [DepartmentCode],
                        [Price],
                        [TransactionDate],
                        [isRefund]
                    FROM
                        [itm].[DepartmentTransactionsByYearMonth]('{department}',{month},{year},1)
                    ORDER BY
                        [TransactionDate] DESC, [Price] DESC
                        """
                department_refunds = TransactionModel.get_transaction_by(refund_query)
                month_name = BillingModel.get_billing_month_name(int(month))
                return render_template('transaction.html', transactions=department_transactions,
                                       refunds=department_refunds,
                                       transaction_title=f'Orders for department code {department} for {month_name} {year}',
                                       refunds_title=f'Refunds for department code {department} for {month_name} {year}')
    return redirect(url_for('admin.Admin'))


@admin.route('/admin/billing/email/<year>/<month>', methods=['GET'])
def email_finance_report(year, month):
    if request.method == 'GET':
        if 'privilege' in session:
            if session['privilege'] in [2, 3]:
                email = Email()
                email.set_recipients(
                    ['N0692013@my.ntu.ac.uk', 'ublavins@gmail.com'])
                info = email.send_finance_report(BillingModel.get_billing_month_name(int(month)), year)
                flash(info)
    return redirect(url_for('admin.billing'))


