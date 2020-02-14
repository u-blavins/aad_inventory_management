import pytest
from mock import MagicMock, patch

from models.Transaction import Transaction


class TestTransaction:
    """ Test Suite for Transaction Model """

    def setup_method(self):
        self.mock_transaction = Transaction()
        
    def test_set_get_transaction_id(self):
        """ Test Success: Transaction id set and get """
        fake_trans_id = 'trans_id'
        self.mock_transaction.set_transaction_id(fake_trans_id)
        sut = self.mock_transaction.get_transaction_id()
        assert sut == fake_trans_id

    def test_get_transaction_id(self):
        """ Test Success: Transaction id returns None if not been set """
        fake_transaction = Transaction()
        sut = fake_transaction.get_transaction_id()
        assert sut == None

    def test_set_get_user_id(self):
        """ Test Success: User id set and get """
        fake_user_id = 'user_id1'
        self.mock_transaction.set_user_id(fake_user_id)
        sut = self.mock_transaction.get_user_id()
        assert sut == fake_user_id

    def test_set_get_department_code(self):
        """ Test Success: Department code set and get """
        fake_department_code = 'dept_code1'
        self.mock_transaction.set_department_code(fake_department_code)
        sut = self.mock_transaction.get_department_code()
        assert sut == fake_department_code

    def test_set_get_price(self):
        """ Test Success: Price set and get """
        fake_price = 23.0
        self.mock_transaction.set_price(fake_price)
        sut = self.mock_transaction.get_price()
        assert sut == fake_price

    def test_set_get_transaction_date(self):
        fake_transaction_date = '11/02/2020'
        self.mock_transaction.set_transaction_date(fake_transaction_date)
        sut = self.mock_transaction.get_transaction_date()
        assert sut == fake_transaction_date

    def test_set_get_refund(self):
        fake_refund = 0
        self.mock_transaction.set_refund(fake_refund)
        sut = self.mock_transaction.get_refund()
        assert sut == fake_refund

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 'refund'),
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 'refund')
    ], autospec=True)
    def test_get_all_transactions_returns_transactions_in_db(self, mock_connect, mock_execute):
        """ Test Success: """
        sut = Transaction.get_all_transactions()
        assert isinstance(sut, list)
        assert len(sut) == 2
    
    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_transactions_returns_empty_if_no_transactions_in_db(self, mock_connect, mock_execute):
        """ Test Failure: """
        sut = Transaction.get_all_transactions()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id3', 'user_id4', 'dept_code2', 'price', 'transaction_date', 1)
    ], autospec=True)
    def test_get_transaction_returns_transaction_if_exists(self, mock_connect, mock_execute):
        """ Test Success: """
        fake_trans_id = 'trans_id3'
        sut = Transaction.get_transaction(fake_trans_id)
        assert isinstance(sut, Transaction)
        assert sut.get_transaction_id() == 'trans_id3'
    
    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_transaction_returns_empty_if_transaction_does_not_exist(self, mock_connect, mock_execute):
        """ Test Failure: """
        fake_trans_id = 'trans_id'
        sut = Transaction.get_transaction(fake_trans_id)
        assert sut == None

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0),
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0)
    ], autospec=True)
    def test_get_transaction_by_returns_transactions_based_on_query(self, mock_connect, mock_execute):
        """ Test Success: """
        fake_query = 'query'
        sut = Transaction.get_transaction_by(fake_query)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_transaction_by_returns_empty_if_query_returns_empty(self, mock_connect, mock_execute):
        """ Test Failure: """
        fake_query = 'query'
        sut = Transaction.get_transaction_by(fake_query)
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0),
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0)
    ], autospec=True)
    def test_get_all_user_transactions_returns_transactions_if_user_has_transactions(self, mock_connect, mock_execute):
        """ Test Success: """
        fake_user_id = 'user_id1'
        fake_refund = 0
        sut = Transaction.get_all_user_transactions(fake_user_id, fake_refund)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_user_transactions_returns_empty_if_user_has_no_transactions(self, mock_connect, mock_execute):
        """ Test Failure: """
        fake_user_id = 'user_id'
        fake_refund = 0
        sut = Transaction.get_all_user_transactions(fake_user_id, fake_user_id)
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0),
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0)
    ], autospec=True)
    def test_get_all_department_transactions_returns_transactions_for_a_department(self, mock_connect, mock_execute):
        """ Test Success: """
        fake_dept_id = 'dept_code1'
        sut = Transaction.get_all_department_transactions(fake_dept_id)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_department_transactions_returns_empty_if_department_has_no_transactions(self, mock_connect, mock_execute):
        """ Test Failure: """
        fake_dept_id = 'dept_id'
        sut = Transaction.get_all_department_transactions(fake_dept_id)
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0),
        ('trans_id1', 'user_id1', 'dept_code1', 'price', 'transaction_date', 0)
    ], autospec=True)
    def test_get_all_transactions_by_refund_returns_all_refunded_transactions(self, mock_connect, mock_execute):
        """ Test Success: """
        fake_refund = 0
        sut = Transaction.get_all_transactions_by_refund(fake_refund)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Transaction.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Transaction.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_transactions_by_refund_returns_empty_if_no_refund_transactions(self, mock_connect, mock_execute):
        """ Test Failure: """
        fake_refund = 0
        sut = Transaction.get_all_transactions_by_refund(fake_refund)
        assert isinstance(sut, list)
        assert len(sut) == 0


        