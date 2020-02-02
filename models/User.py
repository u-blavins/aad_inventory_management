from utils import Database

class User:
    """ User Model """

    @staticmethod
    def getAllUsers():
        query = "SELECT * FROM [StoreManagement].[usr].[User]"
        rows = Database.get_rows(query)
        users = []

        for row in rows:
            print(row)
            
        return users

    @staticmethod
    def getUser(id):
        user = User()
        return user

    @staticmethod
    def getUserBy(key, value):
        users = []
        return users


    def __init__(self):
        self.id = None
        self.user = {}
        return

    def setId(self, id):
        self.id = id
        return self

    def getId(self):
        return self.id

    def setEmail(self, email):
        self.user['email'] = email
        return self
    
    def getEmail(self):
        return self.user['email']

    def setFirstName(self, fname):
        self.user['first_name'] = fname
        return self

    def getFirstName(self):
        return self['first_name']

    def setLastName(self, lname):
        self.user['last_name'] = lname
        return self

    def getLastName(self):
        return self.user['last_name']

    def setDepartmentCode(self, dept_code):
        self.user['dept_code'] = dept_code
        return self
    
    def getDepartmentCode(self):
        return self.user['dept_code']
    
    def setAccountType(self, acc_type):
        self.user['acc_type'] = acc_type
        return self
    
    def getAccountType(self):
        return self.user['acc_type']