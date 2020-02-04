from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify
from utils import Database
from models.Item import Item as ItemModel

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