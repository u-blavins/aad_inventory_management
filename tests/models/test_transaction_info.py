import pytest
from mock import MagicMock, patch

from models.TransactionInfo import TransactionInfo

class TestTransactionInfo:
    """ Test Suite for Transaction Info Model """

    def setup_method(self):
        self.mock_trans_info = TransactionInfo()

    def test_set_get_trans_id(self):
        """ Test Success: Transaction id set and get """
        fake_trans_id = 'trans_id1'
        self.mock_trans_info.set_transaction_id(fake_trans_id)
        sut = self.mock_trans_info.get_transaction_id()
        assert sut == fake_trans_id

    def test_set_get_item_code(self):
        """ Test Success: Transaction item code set and get """
        fake_item_code = 'pen1'
        self.mock_trans_info.set_item_code(fake_item_code)
        sut = self.mock_trans_info.get_item_code()
        assert sut == fake_item_code

    def test_set_get_quantity(self):
        """ Test Success: Transaction quantity set and get """
        fake_quantity = 123
        self.mock_trans_info.set_quantity(fake_quantity)
        sut = self.mock_trans_info.get_quantity()
        assert sut == fake_quantity

    def test_set_get_unit_name(self):
        fake_unit_name = 'test_product'
        self.mock_trans_info.set_unit_name(fake_unit_name)
        sut = self.mock_trans_info.get_unit_name()
        assert sut == fake_unit_name

    def test_set_get_transaction_date(self):
        fake_transaction_date = '20/04/2020'
        self.mock_trans_info.set_transaction_date(fake_transaction_date)
        sut = self.mock_trans_info.get_transaction_date()
        assert sut == fake_transaction_date