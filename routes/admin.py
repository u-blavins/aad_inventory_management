from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

from models.Item import Item as ItemModel

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

@admin.route('/admin/add-item')
def add_stock():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
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
            return render_template('acceptUsers.html')
    return redirect(url_for('admin.Admin'))