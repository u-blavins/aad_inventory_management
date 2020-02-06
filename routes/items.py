from flask import Blueprint, request, jsonify
from models.Item import Item as ItemModel
from models.Unit import Unit as UnitModel

items = Blueprint('items', __name__)


@items.route('/api/items', methods=['GET'])
def get_items():
    result = ItemModel.get_all_items()
    items = []
    for item in result:
        items.append(item.__dict__)
    return jsonify(items=items)


@items.route('/api/items/item/<code>', methods=['GET'])
def get_item(code):
    item = ItemModel.get_item(code)
    return jsonify(item=item.__dict__)


@items.route('/api/items/codes', methods=['GET'])
def get_codes():
    codes = ItemModel.get_codes()
    return jsonify(codes=codes)


@items.route('/api/items/<code>/units', methods=['GET'])
def get_units(code):
    units_collection = ItemModel.get_unit_types(code)
    return jsonify(units=units_collection)


@items.route('/api/items/add')
def add_items():
    code = request.args.get('code')
    name = request.args.get('name')
    risk = request.args.get('risk')
    price = request.args.get('price')
    ItemModel.add_item(code, name, risk, price)
    return {"Message": "Added Item"}


@items.route('/api/units')
def units():
    units_collection = []
    result = UnitModel.get_all_units()
    for unit in result:
        units.append(unit.__dict__)
    return jsonify(units=units_collection)