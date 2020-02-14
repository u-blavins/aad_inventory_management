import pytest
from mock import MagicMock, patch

from models.Billing import Billing


class TestBilling:
    """ Test Suite for Billing Model """

    def setup_method(self):
        self.mock_billing = Billing()

    def test_set_get_department_code(self):
        """ Test Success: Department code set and get """
        fake_dept_code = 'dept_code1'
        self.mock_billing.set_department_code(fake_dept_code)
        sut = self.mock_billing.get_department_code()
        assert sut == fake_dept_code

    def test_get_department_code_returns_none_if_not_set(self):
        """ Test Failure: None returned if department code not set """
        mock_billing = Billing()
        sut = mock_billing.get_department_code()
        assert sut == None

    def test_set_get_billing_month(self):
        """ Test Success: Billing month set and get """
        fake_billing_month = 2
        self.mock_billing.set_billing_month(fake_billing_month)
        sut = self.mock_billing.get_billing_month()
        assert sut == fake_billing_month

    def test_set_get_billing_year(self):
        """ Test Success: Billing year set and get """
        fake_billing_year = 2020
        self.mock_billing.set_billing_year(fake_billing_year)
        sut = self.mock_billing.get_billing_year()
        assert sut == fake_billing_year

    def test_set_get_total(self):
        """ Test Success: Billing year set and get """
        fake_total = 123.45
        self.mock_billing.set_total(fake_total)
        sut = self.mock_billing.get_total()
        assert sut == fake_total

    def test_get_billing_month_name(self):
        """ Test Success: Billing month name returned """
        fake_month = 2
        sut = self.mock_billing.get_billing_month_name(fake_month)
        assert sut == 'February'

    def test_get_billing_month_name_returns_invalid_if_month_incorrectly_entered(self):
        """ Test Failure: Error message returned """
        fake_month = 13
        sut = self.mock_billing.get_billing_month_name(fake_month)
        assert sut == 'Invalid Month'

    @patch('models.Billing.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Billing.Database.execute_query', return_value=[(1, 2020),(2, 2020)], 
            autospec=True)
    def test_get_billing_rows_returns_rows_from_db(self, mock_connect, mock_execute):
        """ Test Success: Billing rows successfully from db """
        sut = Billing.get_billing_rows()
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Billing.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Billing.Database.execute_query', return_value=[], autospec=True)
    def test_get_billing_rows_returns_empty_list_if_no_billing_rows_present(self, mock_connect, mock_execute):
        """ Test Failure: Empty list returned if no billing rows present """
        sut = Billing.get_billing_rows()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Billing.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Billing.Database.execute_query', return_value=[('dept1', 123.12),('dept2', 123.12)], 
            autospec=True)
    def test_get_department_billing_returns_rows(self, mock_connect, mock_execute):
        """ Test Success: Department billing rows successfully from db """
        fake_month = 2
        fake_year = 2020
        sut = Billing.get_department_billing(fake_month, fake_year)
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Billing.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Billing.Database.execute_query', return_value=[], autospec=True)
    def test_get_department_billing_returns_empty_if_no_billings_for_month_and_year(self, mock_connect, mock_execute):
        """ Test Failure: Empty list returned if no billing rows present for month and year """
        fake_month = 4
        fake_year = 2060
        sut = Billing.get_department_billing(fake_month, fake_year)
        assert isinstance(sut, list)
        assert len(sut) == 0