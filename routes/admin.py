from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def Admin():
    session['is_admin'] = ''
    if 'is_admin' not in session:
        return redirect(url_for('auth.Auth'))
    return render_template('admin.html')

@admin.route('/admin/transactions')
def transactions():
    return render_template('generateReport.html')

@admin.route('/admin/restock')
def restock():
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/stocks')
def stocks():
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/product/add')
def add_product():
    return render_template('addItemToInventory.html')

@admin.route('/admin/product/remove')
def remove_product():
    return render_template('removeItemFromInventory.html')
