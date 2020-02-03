from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils import Database

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def Basket():
    if 'basket' not in session:
        session['basket'] = []
    return render_template('basket.html')

@basket.route('/basket/add', methods=['POST'])
def add_items_basket():
    if request.method == 'POST':
        items = request.form.getlist('item[]')
        
    return jsonify(basket=items)

