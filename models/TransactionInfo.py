from utils.Database import Database

class TransactionInfo:
    """ TransactionInfo Model """

    @staticmethod
    def get_user_transactions(id):
        trans_info = []

        query = """
        SELECT 
            ti.[TransactionID],
            ti.[ItemCode],
            ti.[Quantity],
            ti.[UnitName],
            t.[TransactionDate]
            FROM [itm].[TransactionInfo] ti
            INNER JOIN [itm].[Transaction] t ON
                ti.[TransactionID] = t.[TransactionID]
            WHERE 
                t.[isRefund] = 0
            AND
                t.[UserID] = '%s'
        """ % id

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        for row in rows:
            info = TransactionInfo()
            info.set_transaction_id(row[0])
            info.set_item_code(row[1])
            info.set_quantity(row[2])
            info.set_unit_name(row[3])
            trans_info.append(info)
        
        return trans_info

    def __init__(self):
        self.transactions = {}
        return
    
    def set_transaction_id(self, id):
        self.transactions['transaction_id'] = id
        return self

    def get_transaction_id(self):
        return self.transactions['transaction_id']

    def set_item_code(self, item):
        self.transactions['item_code'] = item
        return self

    def get_item_code(self):
        return self.transactions['item_code']

    def set_quantity(self, quantity):
        self.transactions['quantity'] = quantity
        return self

    def get_quantity(self):
        return self.transactions['quantity']

    def set_unit_name(self, unit):
        self.transactions['unit'] = unit
        return self
    
    def get_unit_name(self):
        return self.transactions['unit']
