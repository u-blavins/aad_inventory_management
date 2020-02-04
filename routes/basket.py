from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils import Database

from models.Item import Item as ItemModel

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def Basket():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    if 'basket' not in session:
        session['basket'] = []
    return render_template('basket.html')

@basket.route('/add-item')
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    return render_template('addItem.html')

@basket.route('/basket/add', methods=['POST'])
def add_items_basket():
    if request.method == 'POST':
        items = {}
        codes = request.form.getlist('codes[]')
        present_codes = ItemModel.get_codes()
        quantity = request.form.getlist('quantity[]')
        if len(codes) == len(quantity):
            for i in range(len(codes)):
                if codes[i] in present_codes:
                    if codes[i] not in items:
                        items[codes[i]] = int(quantity[i])
                    else:
                        items[codes[i]] += int(quantity[i])
    return jsonify(items=items)

