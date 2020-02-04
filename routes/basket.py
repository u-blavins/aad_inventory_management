from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils import Database

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def Basket():
    if 'basket' not in session:
        session['basket'] = []
    return render_template('basket.html')

@basket.route('/add-item')
def add_item():
    return render_template('addItem.html')

@basket.route('/basket/add', methods=['POST'])
def add_items_basket():
    if request.method == 'POST':
        items = {}
        codes = request.form.getlist('codes[]')
        quantity = request.form.getlist('quantity[]')
        if len(codes) == len(quantity):
            for i in range(len(codes)):
                if codes[i] not in items:
                    items[codes[i]] = quantity[i]
                else:
                    items[codes[i]] += quantity
    return jsonify(items=items)

