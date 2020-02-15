import pytest
from mock import MagicMock, patch

from models.ReturnItems import ReturnItems


class TestReturnItems:
    """ Test Suite for Return Items Model """

    def setup_method(self):
        self.mock_return_items = ReturnItems()