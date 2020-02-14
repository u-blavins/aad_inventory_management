from utils.Database import Database
from models.Item import Item as ItemModel


class Basket:
    """ Basket Model """

    def __init__(self, basket):
        self.basket = basket
        return

    def get_basket(self):
        return self.basket

    def get_items(self):
        items = []
        for item in self.basket.keys():
            items.append(item)
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