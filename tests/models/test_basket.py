import pytest
from mock import MagicMock, patch

from models.Basket import Basket


class TestBasket:
    """ Test Suite for the Basket Model """

    def setup_method(self):
        fake_basket = {
            'item1': {
                'units': {
                    'unit_1': 5,
                    'unit_2': 2
                },
                'quantity': 15
            }
        }
        self.mock_basket = Basket(fake_basket)
    
    def test_get_basket_returns_dict_of_basket(self):
        """ Test Success: Dict returned of basket """
        sut = self.mock_basket.get_basket()
        assert sut == {'item1': {'units': {'unit_1': 5,
                    'unit_2': 2},'quantity': 15}}

    def test_get_items_returns_list_of_items_in_basket(self):
        """ Test Success: List of items returned """
        sut = self.mock_basket.get_items()
        assert isinstance(sut, list)
        assert len(sut) == 1

    def test_get_units_returns_dict_of_item_units(self):
        """ Test Success: Dict of item units returned from basket """
        fake_item = 'item1'
        sut = self.mock_basket.get_units(fake_item)
        assert {'unit_1': 5, 'unit_2': 2}

    def test_get_quantity_returns_number_of_items(self):
        """ Test Success: Quantity of item returned """
        fake_item = 'item1'
        sut = self.mock_basket.get_quantity(fake_item)
        assert sut == 15
