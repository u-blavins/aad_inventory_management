import pytest
from mock import MagicMock, patch

from models.Unit import Unit

class TestUnit:
    """ Test Suite for Unit Model """

    def setup_method(self):
        self.mock_unit = Unit()

    def test_set_get_name(self):
        """ Test Success: Unit name set and get """
        fake_name = 'Single'
        self.mock_unit.set_name(fake_name)
        sut = self.mock_unit.get_name()
        assert sut == fake_name

    def test_get_name(self):
        """ Test Success: Unit name returns none if not set """
        fake_unit = Unit()
        sut = fake_unit.get_name()
        assert sut == None

    def test_set_get_value(self):
        """ Test Success: Unit value set and get """
        fake_value = 1
        self.mock_unit.set_value(fake_value)
        sut = self.mock_unit.get_value()
        assert sut == fake_value

    def test_get_value(self):
        """ Test Success: Unit value returns none if not set """
        fake_unit = Unit()
        sut = fake_unit.get_value()
        assert sut == None

    @patch('models.Unit.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Unit.Database.execute_query', 
            return_value=[('Single', 1), ('Box', 5)], autospec=True)
    def test_get_units_returns_all_units_if_present(self, mock_connect, mock_exec):
        """ Test Success: All Units are returned from db """
        sut = Unit.get_all_units()
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.Unit.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Unit.Database.execute_query', return_value=[], autospec=True)
    def test_get_units_returns_empty_list_if_no_units_present(self, mock_connect, mock_exec):
        """ Test Success: All Units are returned from db """
        sut = Unit.get_all_units()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.Unit.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Unit.Database.execute_query', return_value=[('Single', 1)], autospec=True)
    def test_get_unit_returns_unit_if_exists(self, mock_connect, mock_exec):
        """ Test Success: Unit returned if found """
        fake_name = 'Single'
        sut = Unit.get_unit(fake_name)
        assert isinstance(sut, Unit)
        assert sut.get_name() == 'Single'
        assert sut.get_value() == 1

    @patch('models.Unit.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.Unit.Database.execute_query', return_value=[], autospec=True)
    def test_get_unit_returns_none_if_not_exists(self, mock_connect, mock_exec):
        """ Test Failure: Unit returns None if not found """
        fake_name = 'Single'
        sut = Unit.get_unit(fake_name)
        assert sut == None
