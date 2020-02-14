import pytest
from mock import MagicMock, patch

from models.PurchaseOrderInfo import PurchaseOrderInfo


class TestPurchaseOrderInfo:
    """ Test Suite for Purchase Order Info model """

    def setup_method(self):
        self.mock_purchase_order_info = PurchaseOrderInfo()

    def test_set_get_item_code(self):
        """ Test Success: Item code set and get """
        fake_item_code = 'item1'
        self.mock_purchase_order_info.set_item_code(fake_item_code)
        sut = self.mock_purchase_order_info.get_item_code()
        assert sut == fake_item_code

    def test_get_item_code_returns_none_if_not_set(self):
        """ Test Failure: None returned if item code not set """
        fake_purchae_order_info = PurchaseOrderInfo()
        sut = fake_purchae_order_info.get_item_code()
        assert sut == None

    def test_set_get_quantity(self):
        """ Test Success: Quantity set and get """
        fake_quantity = 3
        self.mock_purchase_order_info.set_quantity(fake_quantity)
        sut = self.mock_purchase_order_info.get_quantity()
        assert sut == fake_quantity

    def test_set_get_is_complete(self):
        """ Test Success: Is complete set and get """
        fake_val = 1
        self.mock_purchase_order_info.set_is_complete(1)
        sut = self.mock_purchase_order_info.get_is_complete()
        assert sut == fake_val

    def test_set_get_completion_date(self):
        """ Test Success: Completion date set and get """
        fake_date = '11/02/2020'
        self.mock_purchase_order_info.set_completion_date(fake_date)
        sut = self.mock_purchase_order_info.get_completion_date()
        assert sut == fake_date

    def test_set_get_is_approved_by(self):
        """ Test Success: Approved by set and get """
        fake_approver = 'user1'
        self.mock_purchase_order_info.set_approved_by(fake_approver)
        sut = self.mock_purchase_order_info.get_approved_by()
        assert sut == fake_approver

    @patch('models.PurchaseOrderInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.PurchaseOrderInfo.Database.execute_sproc', return_value=[('Success',)], autospec=True)
    def test_create_purchase_order_info_creates_purchase_order_info(self, mock_connect, mock_execute):
        """ Test Success: Purchase Order Info created and message received back """
        fake_order = 'order1'
        fake_item = 'item1'
        fake_quantity = 3
        fake_cursor = MagicMock()
        sut = PurchaseOrderInfo.create_purchase_order_info(
            fake_order, fake_item, fake_quantity, fake_cursor)
        assert sut == 'Success'

    @patch('models.PurchaseOrderInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.PurchaseOrderInfo.Database.execute_non_query')
    def test_confirm_delivery_confirms_delivery(self, mock_connect, mock_execute):
        """ Test Success: Confirm delviery confirms delivery """
        fake_order = 'order1'
        fake_item = 'item1'
        fake_user = 'user1'
        sut = PurchaseOrderInfo.confirm_delivery(fake_order, fake_item, fake_user)

    @patch('models.PurchaseOrderInfo.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.PurchaseOrderInfo.Database.execute_query', 
            return_value=[('item1', 'quantity', 1, None, None),
            ('item2', 'quantity', 1, '10/02/2020', 'user2')],
            autospec=True)
    def test_get_purchase_order_info_pending_returns_purchase_order_info(self, mock_connect, mock_exec):
        """ Test Success: Purchase Order Info returned"""
        fake_purchase_order_id = 'po1'
        sut = PurchaseOrderInfo.get_purchase_order_info(fake_purchase_order_id)
        assert isinstance(sut, list)
        assert len(sut)== 2
