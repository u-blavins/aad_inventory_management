import pytest
from mock import MagicMock, patch

from models.User import User


class TestUser:
    """ Test Suite for User Model """

    def setup_method(self):
        self.mock_user = User()
    
    def test_set_get_id(self):
        """ Test Success: User id set and get """
        fake_id = 'test_id'
        self.mock_user.set_id(fake_id)
        sut = self.mock_user.get_id()
        assert sut == fake_id

    def test_get_id(self):
        """ Test Failure: User id not set and returns None """
        fake_user = User()
        sut = fake_user.get_id()
        assert sut == None

    def test_set_get_email(self):
        """ Test Success: User email set and get """
        fake_email = 'test@test.com'
        self.mock_user.set_email(fake_email)
        sut = self.mock_user.get_email()
        assert sut == fake_email

    def test_set_get_first_name(self):
        """ Test Success: User first name set and get """
        fake_fname = 'foo'
        self.mock_user.set_first_name(fake_fname)
        sut = self.mock_user.get_first_name()
        assert sut == fake_fname

    def test_set_get_last_name(self):
        fake_lname = 'bar'
        self.mock_user.set_last_name(fake_lname)
        sut = self.mock_user.get_last_name()
        assert sut == fake_lname

    def test_set_get_department_code(self):
        fake_dept_code = 'computer_science'
        self.mock_user.set_department_code(fake_dept_code)
        sut = self.mock_user.get_department_code()
        assert sut == fake_dept_code

    def test_set_get_user_level(self):
        fake_user_level = 0
        self.mock_user.set_user_level(fake_user_level)
        sut = self.mock_user.get_user_level()
        assert sut == fake_user_level

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', 
            return_value=[
                ('user1', 'email1', 'fname1', 'lname1', 'deptcode1', 1), 
                ('user2', 'email2', 'fname2', 'lname2', 'deptcode2', 2)
            ], 
            autospec=True)
    def test_get_all_users_returns_all_users_if_present(self, mock_connect, mock_exec):
        """ Test Success: All Users are returned from db"""
        sut = User.get_all_users()
        assert isinstance(sut, list)
        assert len(sut) == 2

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', return_value=[], autospec=True)
    def test_get_all_users_returns_empty_list_if_no_users_present(self, mock_connect, mock_exec):
        """ Test Success: All Users are returned from db"""
        sut = User.get_all_users()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', 
            return_value=[('user1', 'email1', 'fname1', 'lname1', 'deptcode1', 1)], 
            autospec=True)
    def test_get_user_returns_user_if_exists(self, mock_connect, mock_exec):
        """ Test Success: User are returned if found """
        fake_user_id = 'user1'
        sut = User.get_user(fake_user_id)
        assert isinstance(sut, User)
        assert sut.get_id() == 'user1'
        assert sut.get_first_name() == 'fname1'

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', return_value=[], autospec=True)
    def test_get_user_returns_none_if_user_does_not_exist(self, mock_connect, mock_exec):
        """ Test Success: User are returned if found """
        fake_user_id = 'user3'
        sut = User.get_user(fake_user_id)
        assert sut == None

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', 
            return_value=[('user1', 'email1', 'fname1', 'lname1', 'deptcode1', 1)], 
            autospec=True)
    def test_get_user_by_returns_user_if_key_exists(self, mock_connect, mock_exec):
        """ Test Success: User are returned if key found """
        fake_key = '[Email]'
        fake_value = 'email1'
        sut = User.get_user_by(fake_key, fake_value)
        assert isinstance(sut, User)
        assert sut.get_email() == fake_value
        assert sut.get_first_name() == 'fname1'

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', return_value=[], autospec=True)
    def test_get_user_by_returns_none_if_key_does_not_exist(self, mock_connect, mock_exec):
        """ Test Failure: User are returned if key found """
        fake_key = '[Email]'
        fake_value = 'email3'
        sut = User.get_user_by(fake_key, fake_value)
        assert sut == None

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', 
            return_value=[('user3', 'email3', 'fname3', 'lname3', 'deptcode1', 0)], 
            autospec=True)
    def test_get_user_approvals_returns_users_waiting_for_registration_approval(self, mock_connect, mock_exec):
        """ Test Success: Users returned if in approval """
        sut = User.get_user_approval()
        assert isinstance(sut, list)
        assert len(sut) == 1

    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_query', return_value=[], autospec=True)
    def test_get_user_approvale_returns_empty_list_if_no_registrations(self, mock_connect, mock_exec):
        """ Test Failure: Empty list returned if no user in approval """
        sut = User.get_user_approval()
        assert isinstance(sut, list)
        assert len(sut) == 0

    @patch.object(User, 'get_user', return_value=None)
    def test_update_user_privilege_does_not_update_if_user_does_not_exist(self, mock_user):
        """ Test Failure: No update and message returned when user does not exist """
        fake_user_id = 'user1'
        fake_privilege = '2'
        sut = User.update_user_privilege(fake_user_id, fake_privilege)
        assert sut == 'User not found'

    @patch('models.User.User.get_user')
    def test_update_user_privilege_does_not_update_if_privilege_the_same(
        self, mock_user):
        """ Test Failure: User privilege not updated """
        fake_user_id = 'user1'
        fake_privilege = 1
        user = User()
        user.set_user_level(1)
        mock_user.return_value = user
        sut = User.update_user_privilege(fake_user_id, fake_privilege)
        assert sut == 'User privilege is already set as selected privilege'

    @patch('models.User.User.get_user')
    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_non_query')
    def test_update_user_privilege_updates_user_privilege(
        self, mock_user, mock_connect, mock_exec):
        """ Test Success: User privilege updated """
        fake_user_id = 'user1'
        fake_privilege = 0
        user = User()
        user.set_user_level(1)
        mock_user.return_value = user
        sut = User.update_user_privilege(fake_user_id, fake_privilege)
        assert sut == 'Successfully updated user privilege'

    @patch('models.User.User.get_user')
    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_non_query', side_effect=Exception('test'))
    def test_update_user_privilege_does_not_update_user_privilege_with_exception(
        self, mock_user, mock_connect, mock_exec):
        """ Test Failure: Privilege not updated with excpetion """
        fake_user_id = 'user1'
        fake_privilege = 0
        user = User()
        user.set_user_level(1)
        mock_user.return_value = user
        sut = User.update_user_privilege(fake_user_id, fake_privilege)
        assert sut == 'Error updating user privilege'

    @patch('models.User.User.get_user')
    def test_update_user_password_does_not_update_if_user_does_not_exist(self, mock_user):
        """ Test Failure: No update and message returned when user does not exist """
        fake_user_id = 'user1'
        fake_privilege = 'pass2'
        mock_user.return_value = None
        sut = User.update_user_password(fake_user_id, fake_privilege)
        assert sut == 'User not found'

    @patch('models.User.User.get_user', return_value=User(), autospec=True)
    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_sproc', side_effect=Exception('test'))
    def test_update_user_password_does_not_update_user_password_with_exception(
        self, mock_user, mock_connect, mock_exec):
        """ Test Failure: Password not updated with excpetion """
        fake_user_id = 'user1'
        fake_privilege = 'pass2'
        sut = User.update_user_password(fake_user_id, fake_privilege)
        assert sut == 'Error updating user password'

    @patch('models.User.User.get_user', return_value=User(), autospec=True)
    @patch('models.User.Database.connect', return_value=MagicMock(), autospec=True)
    @patch('models.User.Database.execute_sproc', return_value='Successfully updated password', autospec=True)
    def test_update_user_password_updates_user_password(
        self, mock_user, mock_connect, mock_exec):
        """ Test Success: User password updated """
        fake_user_id = 'user1'
        fake_privilege = 'pass2'
        sut = User.update_user_password(fake_user_id, fake_privilege)
        assert sut == 'Successfully updated password'