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

    @patch('models.TransactionInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.TransactionInfo.Database.execute_query', 
            return_value=[
                ('item_code1', 4, 'unit1'),
                ('item_code5', 2, 'unit2'),
            ], 
            autospec=True)
    def test_get_transaction_info_returns_all_transaction_info(self, mock_connect, mock_exec):
        """ Test Success: All Transaction info returned based on id """
        fake_trans_id = 'trans_id1'
        sut = TransactionInfo.get_transaction_info(fake_trans_id)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.TransactionInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.TransactionInfo.Database.execute_query', return_value=[], autospec=True)
    def test_get_transaction_info_returns_empty_list_if_transaction_does_not_exist(self, mock_connect, mock_exec):
        """ Test Failure: Empty list returned if transaction id does not exist """
        fake_trans_id = 'trans_id1'
        sut = TransactionInfo.get_transaction_info(fake_trans_id)
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.TransactionInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.TransactionInfo.Database.execute_query', 
            return_value=[
                ('trans_id1', 'item_code1', 4, 'unit1', '11/02/2020'),
                ('trans_id1', 'item_code5', 2, 'unit2', '11/02/2020')
            ], 
            autospec=True)
    def test_get_user_transactions_returns_all_transaction_info(self, mock_connect, mock_exec):
        """ Test Success: All Transaction info returned based on id """
        fake_user_id = 'user_id1'
        sut = TransactionInfo.get_user_transactions(fake_user_id)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.TransactionInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.TransactionInfo.Database.execute_query', return_value=[], autospec=True)
    def test_get_user_transactions_returns_empty_list_if_transaction_does_not_exist(self, mock_connect, mock_exec):
        """ Test Failure: Empty list returned if user does not have transactions """
        fake_user_id = 'user_id1'
        sut = TransactionInfo.get_user_transactions(fake_user_id)
        assert isinstance(sut, list)
        assert len(sut) == 0