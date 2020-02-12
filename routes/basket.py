from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify, flash
from utils.Database import Database
from utils import Basket as BasketControl

from models.Item import Item as ItemModel
from models.Basket import Basket as BasketModel

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
        
        messages = []

        item = session['basket']

        present_codes = ItemModel.get_codes()
        codes = request.form.getlist('codes[]')
        quantity = request.form.getlist('quantity[]')
        units = request.form.getlist('unitType[]')

        if len(codes) == len(quantity):
            for i in range(len(codes)):
                code = codes[i].upper()
                if code in present_codes:
                    if units[i] in ItemModel.get_unit_types(code):
                        if code not in item:
                            if ItemModel.is_risk_item(code) and session['privilege'] == 0:
                                resp = {'Status':400}
                                message = f'Not able to add {code} to basket'
                                messages.append(message)
                                flash(message)
                            else:
                                resp = BasketControl.get_quantity(code, units[i], int(quantity[i]), 0)

                            if resp['Status'] == 200:
                                item[code] = \
                                    {
                                        'units': {
                                            units[i]: int(quantity[i])
                                        },
                                        'quantity': int(resp['Info'])
                                    }
                                message = f'Successfully added {code} to basket'
                                flash(message)

                            else:
                                message = f'{code}: {units[i]} not able to add more than in stock'
                                messages.append(message)
                                flash(message)

                        else:
                            resp = BasketControl.get_quantity(
                                code, units[i], int(quantity[i]), item[code]['quantity'])
                            if resp['Status'] == 200:
                                if units[i] not in item[code]['units']:
                                    item[code]['units'][units[i]] = int(quantity[i])
                                else:
                                    item[code]['units'][units[i]] += int(quantity[i])
                                item[code]['quantity'] = resp['Info']
                                message = f'Successfully added {code} to basket'
                                flash(message)
                            else: 
                                message = f'{code}: {units[i]} not able to add more than in stock'
                                messages.append(message)
                                flash(message)
                    else:
                        message = f'{code} does not have a unit type of {units[i]}'
                        messages.append(message)
                        flash(message)
                else:
                    message = f'{code} not within the store and has not been added to basket'
                    messages.append(message)
                    flash(message)
            session['basket'] = item
            if len(messages) == 0:
                return redirect(url_for('basket.Basket'))
    return redirect(url_for('basket.add_item'))


@basket.route('/basket/check-out')
def checkout():
    info = {'info': 'Transaction not made'}
    if 'user_id' in session and 'basket' in session:
        if session['basket'] != {}:
            conn = Database.connect()
            cursor = conn.cursor()
            basket = session['basket']
            sproc = "[itm].[createTransaction] @UserID = ?, @Price = ?, @isRefund = ?"
            params = (session['user_id'], BasketControl.get_price(basket), 0)
            trans_id = Database.execute_sproc(sproc, params, cursor)
            cursor.commit()
            for item in basket:
                for unit in basket[item]['units']:
                    sproc = """
                        [itm].[createTransactionInfo] @ItemCode = ?, @TransactionID = ?, @UnitName = ?,
                        @Quantity = ?
                    """
                    params = (
                        item, trans_id[0][0], unit, basket[item]['units'][unit]
                    )
                    result = Database.execute_sproc(sproc, params, cursor)
                    cursor.commit()
                    info['info'] = result[0][0]
            return redirect('/basket/receipt/%s' % trans_id[0][0])
            conn.close()
    return redirect(url_for('basket.Basket'))


@basket.route('/basket/receipt/<trans_id>')
def receipt(trans_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.Auth'))
    if 'basket' not in session:
        session['basket'] = {}
    basket = []
    price = {'total': 0.00}
    transaction = {'id': trans_id}
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
    session['basket'] = {}
    return render_template('receipt.html', basket=basket, price=price, transaction=transaction)
