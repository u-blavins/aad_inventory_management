from models.Item import Item as ItemModel
from models.Unit import Unit as UnitModel

def get_quantity(item, unit, quantity, in_basket):
    """ Return quantity """
    stock_level = ItemModel.get_item(item).get_quantity()
    unit_vol = UnitModel.get_unit(unit).get_value()
    total = unit_vol * quantity
    total += in_basket

    response = {}

    if total > stock_level:
        response = {
            'Status': 400,
            'Info': '%s: Added more than stock' % item
        }
    else:
        response = {
            'Status': 200,
            'Info': total
        }

    return response

def remove_quantity(unit, quantity):
    """ Return remove quantity """
    unit_vol = UnitModel.get_unit(unit).get_value()
    total = unit_vol * int(quantity)
    return total


def get_price(items):
    """ Return price """
    price = 0
    for item in items:
        model = ItemModel.get_item(item)
        price += (model.get_price() * items[item]['quantity'])
    return price