from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def Admin():
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

@admin.route('/admin/add-product')
def add_product():
    return redirect(url_for('admin.Admin'))

@admin.route('/admin/remove-product')
def remove_product():
    return redirect(url_for('admin.Admin'))
