from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils import Database

from models.Item import Item as ItemModel

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def Basket():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    if 'basket' not in session:
        session['basket'] = {}
    basket = session['basket']
    return render_template('basket.html', basket=basket)

@basket.route('/add-item')
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    return render_template('addItem.html')

@basket.route('/basket/order', methods=['POST'])

@basket.route('/basket/add', methods=['POST'])
def add_items_basket():
    if request.method == 'POST':
        if 'basket' not in session:
            session['basket'] = {}
        item = session['basket']
        present_codes = ItemModel.get_codes()
        codes = request.form.getlist('codes[]')
        quantity = request.form.getlist('quantity[]')
        units = request.form.getlist('unitType[]')
        if len(codes) == len(quantity):
            for i in range(len(codes)):
                if codes[i] in present_codes:
                    if codes[i] not in item:
                        item[codes[i]] = {
                            'quantity': int(quantity[i]),
                            'unit': units[i]
                        }
                    else:
                        item[codes[i]]['quantity'] += int(quantity[i])
        session['basket'] = item
    # return redirect(url_for('basket.add_item'))
    return jsonify(basket=session['basket'])

