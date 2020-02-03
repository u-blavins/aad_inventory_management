from utils import Database

class Item:
    """ Item Model """

    @staticmethod
    def getAllItems():
        query = "SELECT * FROM [StoreManagement].[itm].[Item]"
        rows = Database.get_rows(query)
        item = []

        for row in rows:
            print(row)

        return item

    @staticmethod
    def getItem(id):
        item = Item()
        return item

    @staticmethod
    def getItemsBy(key, value):
        item = []
        return item

    def __init__(self):
        self.Code = None
        self.item = {}
        return

    def Insert(self):
        if self.Code == None:
            Database.execute(
                "INSERT INTO [StoreManagement].[itm].[Item] ('code', 'name', 'variant', 'unit_name', 'risk', 'price') VALUES (%s, %s, %s, %s, %s, %s)",
                (self.item['code'], self.item['name'], self.item['variant'], self.item['unit_name'], self.item['risk'], self.item['price']))

            rows = Database.get_rows('SELECT LAST_INSERT_ID() AS insert_id')
            self.Code = rows[0]['insert_id']

    def Delete(self):
        if self.Code == None:
            return
        else:
            Database.execute("DELETE FROM [StoreManagement].[itm].[Item] WHERE Code = %s", (self.Code,))

    def setCode(self, code):
        self.item['code'] = code
        return self

    def getCode(self):
        return self.item['code']

    def setName(self, name):
        self.item['name'] = name
        return self

    def getName(self):
        return self.item['val']

    def setVariant(self, variant):
        self.item['variant'] = variant
        return self

    def getVariant(self):
        return self.item['variant']

    def setUnitName(self, unit_name):
        self.item['unit_name'] = unit_name
        return self

    def getUnitName(self):
        return self.item['unit_name']

    def setRisk(self, risk):
        self.item['risk'] = risk
        return self

    def getRisk(self):
        return self.item['risk']

    def setPrice(self, price):
        self.item['price'] = price
        return self

    def getPrice(self):
        return self.item['price']
