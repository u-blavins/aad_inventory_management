import pytest
from mock import MagicMock, patch

from models.Item import Item


class TestItem:
    """ Test Suite for Item Model """

    def setup_method(self):
        self.mock_item = Item()

    def test_set_get_code(self):
        """ Test Success: Item code set and get """
        fake_code = 'item1'
        self.mock_item.set_code(fake_code)
        sut = self.mock_item.get_code()
        assert sut == fake_code

    def test_get_code_returns_none_if_not_set(self):
        """ Test Failure: None returned if item code not set """
        fake_item = Item()
        sut = fake_item.get_code()
        assert sut == None

    def test_set_get_name(self):
        """ Test Success: Item name set and get """
        fake_item_name = 'item_name'
        self.mock_item.set_name(fake_item_name)
        sut = self.mock_item.get_name()
        assert sut == fake_item_name

    def test_set_get_risk(self):
        """ Test Success: Item risk level set and get """
        fake_is_risk = True
        self.mock_item.set_risk(fake_is_risk)
        sut = self.mock_item.get_risk()
        assert sut

    def test_set_get_price(self):
        """ Test Success: Item price set and get """
        fake_price = 123.12
        self.mock_item.set_price(fake_price)
        sut = self.mock_item.get_price()
        assert sut == fake_price

    def test_set_get_quantity(self):
        """ Test Success: Item quantity set and get """
        fake_quantity = 20
        self.mock_item.set_quantity(fake_quantity)
        sut = self.mock_item.get_quantity()
        assert sut == fake_quantity

    def test_set_get_threshold(self):
        """ Test Success: Item threshold set and get """
        fake_threshold = 10
        self.mock_item.set_threshold(fake_threshold)
        sut = self.mock_item.get_threshold()
        assert sut == fake_threshold

    def test_set_get_purchase_order(self):
        """ Test Success: Item auto purchase order set and get """
        fake_is_auto_purchase_order = 0
        self.mock_item.set_purchase_order(fake_is_auto_purchase_order)
        sut = self.mock_item.get_purchase_order()
        assert sut == fake_is_auto_purchase_order

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[
            ('item1', 'item_1', 1, 123.12, 15, 15, 0),
            ('item2', 'item_2', 0, 123.12, 15, 15, 0)
            ], 
            autospec=True)
    def test_get_all_items_returns_items_from_db(self, mock_connect, mock_execute):
        """ Test Success: Items returned from db """
        sut = Item.get_all_items()
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_items_returns_empty_list_if_no_items_exist(self, mock_connect, mock_execute):
        """ Test Failure: Empty list returned if no items present """
        sut = Item.get_all_items()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[
            ('item1', 'item_1', 1, 123.12, 15, 15, 0)], autospec=True)
    def test_get_item_returns_item_if_exists(self, mock_connect, mock_execute):
        """ Test Success: Item returned if exists """
        fake_item_code = 'item1'
        sut = Item.get_item(fake_item_code)
        assert isinstance(sut, Item)
        assert sut.get_code() == fake_item_code

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[], autospec=True)
    def test_get_item_returns_none_if_not_exists(self, mock_connect, mock_execute):
        """ Test Failure: None returned if item does not exist """
        fake_item_code = 'item2'
        sut = Item.get_item(fake_item_code)
        assert sut == None

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[
            ('item1'), ('item2'), ('item4')], autospec=True)
    def test_get_codes_returns_item_codes_from_db(self, mock_connect, mock_execute):
        """ Test Success: Item rcodes returned """
        sut = Item.get_codes()
        assert isinstance(sut, list)
        assert len(sut) == 3

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[], autospec=True)
    def test_get_item_returns_empty_list_if_no_items_exist(self, mock_connect, mock_execute):
        """ Test Failure: Empty list returned if no items exist """
        sut = Item.get_codes()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_non_query')
    def test_add_item_adds_item_to_db(self, mock_connect, mock_execute):
        """ Test Success: Item added """
        sut = Item.add_item('item3', 'item_3', 15, 123.12, 15, ['Single', 'Box'], 0, 1)

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_non_query')
    def test_delete_item_removes_item_from_display(self, mock_connect, mock_execute):
        """ Test Success: Item added """
        sut = Item.delete_item('item3')

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_non_query')
    def test_edit_item_edit_item_and_returns_to_db(self, mock_connect, mock_execute):
        """ Test Success: Item edited """
        sut = Item.edit_item('item3', 'item_3', 15, 123.12, 15, ['Single', 'Box'], 0)

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[('0')], autospec=True)
    def test_is_risk_item_returns_bit_if_item_exists(self, mock_connect, mock_execute):
        """ Test Success: Risk value returned """
        sut = Item.is_risk_item('item1')
        assert sut == '0'

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[], autospec=True)
    def test_is_risk_item_returns_none_if_item_does_not_exist(self, mock_connect, mock_execute):
        """ Test Failure: None returned if item does not exist """
        sut = Item.is_risk_item('item3')
        assert sut == None

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[('unit1'), ('unit2')], autospec=True)
    def test_get_unit_types_returns_unit_types_for_item(self, mock_connect, mock_execute):
        """ Test Success: Risk value returned """
        fake_item_code = 'item9'
        sut = Item.get_unit_types(fake_item_code)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Item.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Item.Database.execute_query', return_value=[], autospec=True)
    def test_get_unit_types_returns_empty_list_if_item_does_not_exist(self, mock_connect, mock_execute):
        """ Test Failure: Empty list returned if no items exist """
        fake_item_code = 'item3'
        sut = Item.get_unit_types(fake_item_code)
        assert isinstance(sut, list)
        assert len(sut) == 0
    

    
    
