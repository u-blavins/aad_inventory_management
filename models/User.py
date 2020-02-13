from utils.Database import Database


class User:
    """ User Model """

    @staticmethod
    def get_all_users():
        query = """SELECT  
                        [ID]
                        ,[Email]
                        ,[FirstName]
                        ,[LastName] 
                        ,[DepartmentCode]
                        ,[Privileges]
                    FROM
                        [usr].[User]"""
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        users = []

        if rows != []:
            for row in rows:
                user = User()
                user.set_id(row[0])
                user.set_email(row[1])
                user.set_first_name(row[2])
                user.set_last_name(row[3])
                user.set_department_code(row[4])
                user.set_user_level(row[5])
                users.append(user)
            
        return users

    @staticmethod
    def get_user(id):
        user = None

        query = """
        SELECT [ID], [Email], [FirstName], [LastName], [DepartmentCode],
        [Privileges] FROM [usr].[User] WHERE [ID] = '%s'
        """ % id
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        
        if rows != []:
            for row in rows:
                user = User()
                user.set_id(row[0])
                user.set_email(row[1])
                user.set_first_name(row[2])
                user.set_last_name(row[3])
                user.set_department_code(row[4])
                user.set_user_level(row[5])

        return user

    @staticmethod
    def get_registered_users():
        users = []

        query = f"""
        SELECT [ID], [Email], [FirstName], [LastName], [DepartmentCode],
        [Privileges] FROM [usr].[User] WHERE [isApproved] = 1
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        
        if rows != []:
            for row in rows:
                user = User()
                user.set_id(row[0])
                user.set_email(row[1])
                user.set_first_name(row[2])
                user.set_last_name(row[3])
                user.set_department_code(row[4])
                user.set_user_level(row[5])
                users.append(user)

        return users

    @staticmethod
    def get_user_by(key, value):
        user = None

        query = f"""
        SELECT [ID], [Email], [FirstName], [LastName], [DepartmentCode],
        [Privileges] FROM [usr].[User] WHERE {key} = '{value}'
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        
        if rows != []:
            for row in rows:
                user = User()
                user.set_id(row[0])
                user.set_email(row[1])
                user.set_first_name(row[2])
                user.set_last_name(row[3])
                user.set_department_code(row[4])
                user.set_user_level(row[5])

        return user

    @staticmethod
    def get_user_approval():
        users = []

        query = """
            SELECT [ID], [Email], [FirstName], [LastName], [DepartmentCode], [Privileges]
            FROM [StoreManagement].[usr].[WaitingForApproval]                        
            """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                user = User()
                user.set_id(row[0])
                user.set_email(row[1])
                user.set_first_name(row[2])
                user.set_last_name(row[3])
                user.set_department_code(row[4])
                user.set_user_level(row[5])
                users.append(user)

        return users

    @staticmethod
    def update_user_privilege(id, privilege):
        message = 'User not found'
        user = User.get_user(id)
        if user != None:
            if privilege != user.get_user_level():
                query = """
                UPDATE [StoreManagement].[usr].[User] SET [Privileges] = '%s' WHERE [ID] = '%s'
                """ % (privilege, id)
                conn = Database.connect()
                try:
                    cursor = conn.cursor()
                    Database.execute_non_query(query, cursor)
                    cursor.commit()
                    message = "Successfully updated user privilege"
                except Exception as ex:
                    message = "Error updating user privilege"
                conn.close()
            else:
                message = "User privilege is already set as selected privilege"
        return message

    @staticmethod
    def update_user_password(id, password):
        message = 'User not found'
        user = User.get_user(id)
        if user != None:
            sproc = """ [usr].[updatePassword] @UserID = ?, @Password = ?"""
            params = (id, password)
            conn = Database.connect()
            try:
                cursor = conn.cursor()
                result = Database.execute_sproc(sproc, params, cursor)
                cursor.commit()
                conn.close()
                message = result
            except Exception as e:
                message = "Error updating user password"
        return message

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
        return self.user['first_name']

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
    
    def set_user_level(self, acc_type):
        self.user['acc_type'] = acc_type
        return self
    
    def get_user_level(self):
        return self.user['acc_type']