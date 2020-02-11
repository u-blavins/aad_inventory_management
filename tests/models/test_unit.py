import pytest
from mock import MagicMock, patch

from models.Unit import Unit as UnitModel

class TestUnit:
    """ Test Suite for Unit Model """

    def setup_method(self):
        self.mock_unit = UnitModel()

    def test_set_get_name(self):
        """ Test Success: Unit name set and get """
        fake_name = 'Single'
        self.mock_unit.set_name(fake_name)
        sut = self.mock_unit.get_name()
        assert sut == fake_name

    def test_get_name(self):
        """ Test Success: Unit name returns none if not set """
        fake_unit = UnitModel()
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
        fake_unit = UnitModel()
        sut = fake_unit.get_value()
        assert sut == None

    @patch('models.Unit.Database')
    def test_get_unit_returns_unit_if_exists(self, mock_database):
        """ Test Success: Unit returns None if not found """
        fake_name = 'Single'
        fake_response = [('Single', 1)]
        database = mock_database.return_value
        database.connect.return_value = MagicMock()
        database.execute_query.return_value = fake_response
        sut = UnitModel.get_unit(fake_name)
        assert isinstance(sut, Unit)
        assert sut.get_unit == 'Single'
        assert sut.get_value == 1

    @patch('models.Unit.Database')
    def test_get_unit_returns_none_if_unit_does_not_exist(self, mock_database):
        """ Test Failure: Unit returns None if not found """
        fake_name = 'Single'
        database = mock_database.return_value
        database.connect.return_value = MagicMock()
        database.execute_query.return_value = []
        sut = UnitModel.get_unit(fake_name)
        assert sut == None
