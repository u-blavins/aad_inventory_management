from utils import Database

class Transaction:
    """ Transaction Model """

    @staticmethod
    def getAllTransactions():
        query = "SELECT * FROM [StoreManagement].[itm].[Transaction]"
        rows = Database.get_rows(query)
        transaction = []

        for row in rows:
            print(row)

        return transaction

    @staticmethod
    def getTransaction(id):
        transaction = Transaction()
        return transaction

    @staticmethod
    def getTransaction(key, value):
        item = []
        return item

    def __init__(self):
        self.TransactionID = None
        self.transaction = {}
        return

    def Insert(self):
        if self.TransactionID == None:
            Database.execute(
                "INSERT INTO [StoreManagement].[itm].[Transaction] ('transaction_id', 'user_id', 'item_code', 'quantity', 'transaction_date', 'is_refund') VALUES (%s, %s, %s, %s, %s, %s)",
                (self.item['transaction_id'], self.item['user_id'], self.item['item_code'], self.item['quantity'], self.item['transaction_date'],
                 self.item['is_refund']))

            rows = Database.get_rows('SELECT LAST_INSERT_ID() AS insert_id')
            self.Code = rows[0]['insert_id']

    def Delete(self):
        if self.TransactionID == None:
            return
        else:
            Database.execute("DELETE FROM [StoreManagement].[itm].[Transaction] WHERE TransactionID = %s", (self.TransactionID,))

    def setTransactionID(self, transaction_id):
        self.transaction['transaction_id'] = transaction_id
        return self

    def getTransactionID(self):
        return self.transaction['transaction_id']

    def setUserID(self, user_id):
        self.transaction['user_id'] = user_id
        return self

    def getUserID(self):
        return self.transaction['user_id']

    def setItemCode(self, item_code):
        self.transaction['item_code'] = item_code
        return self

    def getItemCode(self):
        return self.transaction['item_code']

    def setQuantity(self, quantity):
        self.transaction['quantity'] = quantity
        return self

    def getQuantity(self):
        return self.transaction['quantity']

    def setTransactionDate(self, transaction_date):
        self.transaction['transaction_date'] = transaction_date
        return self

    def getTransactionDate(self):
        return self.transaction['transaction_date']

    def setIsRefund(self, is_refund):
        self.transaction['is_refund'] = is_refund
        return self

    def getIsRefund(self):
        return self.transaction['is_refund']
