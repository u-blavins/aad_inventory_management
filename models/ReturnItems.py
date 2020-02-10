from utils.Database import Database

from models.Item import Item as ItemModel
from models.Unit import Unit as UnitModel


class ReturnItems:
    """ Return Items Model """

    def __init__(self):
        self.items = {}
        return

    def set_item(self, item, quantity, unit):
        codes = ItemModel.get_codes()
        item = item.upper()
        if item not in self.items:
            if ItemModel.get_item(item) != None:
                if 

        return message
    
    def get_items(self):
        return self.get_items()
            
