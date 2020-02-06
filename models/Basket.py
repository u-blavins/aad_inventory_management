from utils import Database
from models.Item import Item as ItemModel

class Basket:
    """ Basket Model """

    def __init__(self, basket):
        self.basket = basket
        self.total = self.get_total()
        return

    def get_items(self):
        items = []
        items = self.basket.keys()
        return items

    def get_units(self, item):
        units = {}
        if item in self.basket:
            units = self.basket[item]['units']
        return units
    
    def get_quantity(self, item):
        quantity = 0
        if item in self.basket:
            quantity = self.basket[item]['quantity']
        return quantity

    def set_total():
        total = 0
        for item in self.get_items():
            model = ItemModel.get_item(item)
            price += (model.get_price() * self.get_quantity(item))
        return total

    def checkout(self, user):
        sproc = "[itm].[createTransaction] @UserID = ?, @Price = ?, @isRefund = ?"
        params = (user, self.get_total(), 0)
