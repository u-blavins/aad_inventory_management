from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template, session
from models.Item import Item as ItemModel
from models.Unit import Unit as UnitModel

items = Blueprint('items', __name__)


@items.route('/api/items', methods=['GET'])
def get_items():
    if 'user_id' in session:
        result = ItemModel.get_all_items()
        items = []
        for item in result:
            items.append(item.__dict__)
        return jsonify(items=items)


@items.route('/api/items/item/<code>', methods=['GET'])
def get_item(code):
    if 'user_id' in session:
        item = ItemModel.get_item(code)
        return jsonify(item=item.__dict__)


@items.route('/api/items/codes', methods=['GET'])
def get_codes():
    if 'user_id' in session:
        codes = ItemModel.get_codes()
        return jsonify(codes=codes)


@items.route('/api/items/<code>/units', methods=['GET'])
def get_units(code):
    if 'user_id' in session:
        units_collection = ItemModel.get_unit_types(code)
        return jsonify(units=units_collection)


@items.route('/items/add', methods=['POST'])
def add_items():
    if request.method == 'POST':
        code = request.form['code']
        code = code.upper()
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        threshold = request.form['threshold']
        unit_types = request.form.getlist('unitTypes[]')
        risk = request.form['risk']
        purchase = request.form['purchase']
        if code in ItemModel.get_codes():
            flash('Error: Item code "' + str(code) + '" already exists')
            return render_template('addItemToInventory.html')
        if len(unitTypes) == 0:
            flash('Error: At least one unit type required')
            return render_template('addItemToInventory.html')
        else:
            flash('Success: "' + str(code) + '" added to stock')
            ItemModel.add_item(code, name, quantity, price, threshold, unit_types, risk, purchase)
            return redirect(url_for('admin.stocks'))


@items.route('/items/remove/<code>', methods=['POST'])
def remove_item(code):
    if request.method == 'POST':
        if session['privilege'] == 3:
            if code in ItemModel.get_codes():
                ItemModel.delete_item(code)
                flash('Success: Deleted item "' + str(code) + '" ')
            else:
                flash('Error: "' + str(code) + '" does not exist')
    return redirect(url_for('admin.stocks'))


@items.route('/items/edit/<code>', methods=['POST'])
def Edit(code):
    if session['privilege'] in [2, 3]:
        item = ItemModel.get_item(code)
        return render_template('editStock.html', item=item)
    return redirect(url_for('admin.stocks'))


@items.route('/edit/item/<code>', methods=['POST'])
def edit_item(code):
    if request.method == 'POST':
         if session['privilege'] in [2, 3]:
            if code in ItemModel.get_codes():
                name = request.form['name']
                quantity = request.form['quantity']
                price = request.form['price']
                threshold = request.form['threshold']
                risk = request.form['risk']
                purchase_order = request.form['purchase']

                ItemModel.edit_item(code, name, quantity, price, threshold, risk, purchase_order)
                flash('Success: Edited item "' + str(code) + '" ')
            else:
                flash('Error: Could not edit "' + str(code) + '"')
    return redirect(url_for('admin.stocks'))


@items.route('/api/units')
def units():
    units_collection = []
    result = UnitModel.get_all_units()
    for unit in result:
        units.append(unit.__dict__)
    return jsonify(units=units_collection)