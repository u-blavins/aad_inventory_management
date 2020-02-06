from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils import Database
from utils import Basket as BasketControl

from models.Item import Item as ItemModel

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def Basket():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    if 'basket' not in session:
        session['basket'] = {}
    basket = []
    price = {'total': 0.00}
    if len(session['basket']) != 0:
        for item in session['basket']:
            for unit in session['basket'][item]['units']:
                item_model = ItemModel.get_item(item)
                basket_item = {}
                basket_item['code'] = item_model.get_code()
                basket_item['name'] = item_model.get_name()
                basket_item['price'] = item_model.get_price()
                basket_item['unit'] = unit
                basket_item['quantity'] = session['basket'][item]['units'][unit]
                basket.append(basket_item)
        price['total'] = BasketControl.get_price(session['basket'])
    return render_template('basket.html', basket=basket, price=price)

@basket.route('/add-item')
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    return render_template('addItem.html')

@basket.route('/basket/remove/<code>/<unit>/<quantity>')
def remove_from_basket(code, unit, quantity):
    basket = session['basket']
    if code in basket:
        if len(basket[code]['units'].keys()) != 1:
            if unit in basket[code]['units']:
                del basket[code]['units'][unit]
                basket[code]['quantity'] -= BasketControl.remove_quantity(unit, quantity)
        else:
            del basket[code]
    session['basket'] = basket
    return redirect(url_for('basket.Basket'))


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
                    if units[i] in ItemModel.get_unit_types(codes[i]):
                        if codes[i] not in item:
                            resp = BasketControl.get_quantity(codes[i], units[i], int(quantity[i]), 0)
                            if resp['Status'] == 200:
                                item[codes[i]] = \
                                    {
                                        'units': {
                                            units[i]: int(quantity[i])
                                        },
                                        'quantity': int(resp['Info'])
                                    }
                        else:
                            resp = BasketControl.get_quantity(
                                codes[i], units[i], int(quantity[i]), item[codes[i]]['quantity'])
                            if resp['Status'] == 200:
                                if units[i] not in item[codes[i]]['units']:
                                    item[codes[i]]['units'][units[i]] = int(quantity[i])
                                else:
                                    item[codes[i]]['units'][units[i]] += int(quantity[i])
                                item[codes[i]]['quantity'] = resp['Info']
            session['basket'] = item
    return redirect(url_for('basket.Basket'))

@basket.route('/basket/check-out')
def checkout():
    # [itm].[createTransaction] ([UserID], [Department], [Price])
    info = 'Transaction not made'
    if 'user_id' in session and 'basket' in session:
        if session['basket'] != {}:
            basket = session['basket']
            sproc = "[itm].[createTransaction] @UserID = ?, @Price = ?, @isRefund = ?"
            params = (session['user_id'], BasketControl.get_price(basket), 0)
            trans_id = Database.execute_sproc(sproc, params)
            for item in basket:
                for unit in basket[item]['units']:
                    sproc = """
                        [itm].[createTransactionInfo] @ItemCode = ?, @TransactionID = ?, @UnitName = ?,
                        @Qunatity = ?
                    """
                    params = (
                        item, trans_id, unit, session['basket'][item]['units'][unit]
                    )
                    info = Database.execute_sproc(sproc, params)
    return {"Info": info}