from utils import Database

class User:
    """ User Model """

    @staticmethod
    def get_all_users():
        query = "SELECT * FROM [StoreManagement].[usr].[User]"
        rows = Database.get_rows(query)
        users = []

        for row in rows:
            print(row)
            
        return users

    @staticmethod
    def get_user(id):
        user = User()
        return user

    @staticmethod
    def get_user_by(key, value):
        users = []
        return users

    def __init__(self):
        self.id = None
        self.user = {}
        return

    def set_id(self, id):
        self.id = id
        return self

    def get_id(self):
        return self.id

    def set_email(self, email):
        self.user['email'] = email
        return self
    
    def get_email(self):
        return self.user['email']

    def set_first_name(self, fname):
        self.user['first_name'] = fname
        return self

    def get_first_name(self):
        return self['first_name']

    def set_last_name(self, lname):
        self.user['last_name'] = lname
        return self

    def get_last_name(self):
        return self.user['last_name']

    def set_department_code(self, dept_code):
        self.user['dept_code'] = dept_code
        return self
    
    def get_department_code(self):
        return self.user['dept_code']
    
    def set_account_type(self, acc_type):
        self.user['acc_type'] = acc_type
        return self
    
    def get_account_type(self):
        return self.user['acc_type']