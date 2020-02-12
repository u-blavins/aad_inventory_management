from utils.Database import Database


class Transaction:
    """ Transaction Model """

    @staticmethod
    def get_all_transactions():
        transactions = []

        query = """
        SELECT [TransactionID], [UserID], [DepartmentCode],
            [Price], [TransactionDate], [IsRefund] FROM 
            [itm].[Transaction]
        """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])
                transactions.append(transaction)

        return transactions

    @staticmethod
    def get_transaction(transaction_id):
        transaction = None

        query = """
        SELECT [TransactionID], [UserID], [DepartmentCode],
            [Price], [TransactionDate], [IsRefund] FROM 
            [itm].[Transaction] WHERE [TransactionID] = '%s'
        """ % transaction_id

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])

        return transaction

    @staticmethod
    def get_transaction_by(query):
        transactions = []

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])
                transactions.append(transaction)

        return transactions

    @staticmethod
    def get_all_user_transactions(user_id, is_refund):
        transactions = []

        query = f"""
        SELECT [TransactionID], [UserID], [DepartmentCode],
            [Price], [TransactionDate], [IsRefund] FROM 
            [itm].[Transaction] WHERE [UserID] = '{user_id}'
            AND [IsRefund] = {is_refund}
            ORDER BY [TransactionDate] DESC
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])
                transactions.append(transaction)

        return transactions

    @staticmethod
    def get_all_department_transactions(dept_code):
        transactions = []

        query = """
        SELECT [TransactionID], [UserID], [DepartmentCode],
            [Price], [TransactionDate], [IsRefund] FROM 
            [itm].[Transaction] WHERE [DepartmentCode] = '%s'
        """ % dept_code

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])
                transactions.append(transaction)

        return transactions

    @staticmethod
    def get_all_transactions_by_refund(is_refund):
        transactions = []

        query = f"""
        SELECT [TransactionID], [UserID], [DepartmentCode],
            [Price], [TransactionDate], [IsRefund] FROM 
            [itm].[Transaction] WHERE [IsRefund] = {is_refund}
            ORDER BY [TransactionDate] DESC
        """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if rows != []:
            for row in rows:
                transaction = Transaction()
                transaction.set_transaction_id(row[0])
                transaction.set_user_id(row[1])
                transaction.set_department_code(row[2])
                transaction.set_price(row[3])
                transaction.set_transaction_date(row[4])
                transaction.set_refund(row[5])
                transactions.append(transaction)

        return transactions

    def __init__(self):
        self.id = None
        self.transaction = {}
        return

    def set_transaction_id(self, id):
        self.id = id
        return self

    def get_transaction_id(self):
        return self.id

    def set_user_id(self, user_id):
        self.transaction['user_id'] = user_id
        return self

    def get_user_id(self):
        return self.transaction['user_id']

    def set_department_code(self, dept_code):
        self.transaction['dept_code'] = dept_code
        return self

    def get_department_code(self):
        return self.transaction['dept_code']

    def set_price(self, price):
        self.transaction['price'] = price
        return self

    def get_price(self):
        return self.transaction['price']

    def set_transaction_date(self, date):
        self.transaction['date'] = date
        return self

    def get_transaction_date(self):
        return self.transaction['date']

    def set_refund(self, is_refund):
        self.transaction['is_refund'] = is_refund
        return self

    def get_refund(self):
        return self.transaction['is_refund']
