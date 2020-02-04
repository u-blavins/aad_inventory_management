from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def Admin():
    if 'privilege' in session:
        if session['privilege'] in [2, 3]:
            return render_template('admin.html')
    return redirect(url_for('auth.Auth'))

@admin.route('/admin/transactions')
def transactions():
    return render_template('generateReport.html')

@admin.route('/admin/purchase-order')
def purchase_order():
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/stock')
def stocks():
    return render_template('viewStock.html')

@admin.route('/admin/return')
def return_items():
    return render_template('returnItems.html')
