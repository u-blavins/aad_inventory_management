from utils import Database

class Stock:
    """ Stock Model """

    @staticmethod
    def getAllStock():
        query = "SELECT * FROM [StoreManagement].[itm].[Stock]"
        rows = Database.get_rows(query)
        stock = []

        for row in rows:
            print(row)

        return stock

    @staticmethod
    def getStock(id):
        stock = Stock()
        return stock

    @staticmethod
    def getStockBy(key, value):
        stock = []
        return stock

    def __init__(self):
        self.StockCode = None
        self.stock = {}
        return

    def Insert(self):
        if self.StockCode == None:
            Database.execute("INSERT INTO [StoreManagement].[itm].[Stock] ('stock_code', 'item_code', 'quantity', 'unit_name', 'min_threshold', 'max_threshold') VALUES (%s, %s, %s, %s, %s, %s)", (self.stock['item_code'], self.stock['quantity'], self.stock['unit_name'], self.stock['min_threshold'], self.stock['max_threshold'], self.StockCode))

            rows = Database.get_rows('SELECT LAST_INSERT_ID() AS insert_id')
            self.StockCode = rows[0]['insert_id']

    def Delete(self):
        if self.StockCode == None:
            return
        else:
            Database.execute("DELETE FROM [StoreManagement].[itm].[Stock] WHERE StockCode = %s", (self.StockCode,))

    def setStockCode(self, stockcode):
        self.stock['stock_code'] = stockcode
        return self

    def getStockCode(self):
        return self.stock['stock_code']

    def setItemCode(self, itemcode):
        self.stock['item_code'] = itemcode
        return self

    def getItemCode(self):
        return self.stock['item_code']

    def setQuantity(self, quantity):
        self.stock['quantity'] = quantity
        return self

    def getQuantity(self):
        return self.stock['quantity']

    def setUnitName(self, unitname):
        self.stock['unit_name'] = unitname
        return self

    def getUnitName(self):
        return self.stock['unit_name']

    def setMinThreshold(self, minthreshold):
        self.stock['min_threshold'] = minthreshold
        return self

    def getMinThreshold(self):
        return self.stock['min_threshold']

    def setMaxThreshold(self, maxthreshold):
        self.stock['max_threshold'] = maxthreshold
        return self

    def getMaxThreshold(self):
        return self.stock['max_threshold']

