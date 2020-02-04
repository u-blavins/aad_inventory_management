from flask import Blueprint, request, render_template, redirect, session, url_for, jsonify
from utils import Database
from models.Item import Item as ItemModel

import json

items = Blueprint('items', __name__)

@items.route('/api/items', methods=['GET'])
def get_items():
    result = ItemModel.get_all_items()
    items = []
    for item in result:
        items.append(item)
    return items

@items.route('/api/items/item/<code>', methods=['GET'])
def get_item(code):
    item = ItemModel.get_item(code)
    return jsonify(item=item.__dict__)

@items.route('/api/items/codes', methods=['GET'])
def get_codes():
    codes = ItemModel.get_codes()
    return jsonify(codes=codes)