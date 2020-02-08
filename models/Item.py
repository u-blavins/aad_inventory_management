from utils.Database import Database


class Item:
    """ Item Model """

    @staticmethod
    def get_all_items():
        query = """
            SELECT [Code],
            [Name],
            [Risk],
            [Price],
            [Quantity],
            [MinThreshold]
            FROM [StoreManagement].[itm].[Item]
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        items = []

        for row in rows:
            item = Item()
            item.set_code(row[0])
            item.set_name(row[1])
            item.set_risk(row[2])
            item.set_price(row[3])
            item.set_quantity(row[4])
            item.set_threshold(row[5])
            items.append(item)

        return items

    @staticmethod
    def get_item(code):
        item = None

        query = """
        SELECT [Code], [Name], [Risk], [Price],
            [Quantity],
            [MinThreshold] FROM
        [itm].[Item] WHERE [Code] = '%s'
        """ % code

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        for row in rows:
            item = Item()
            item.set_code(row[0])
            item.set_name(row[1])
            item.set_risk(row[2])
            item.set_price(row[3])
            item.set_quantity(row[4])
            item.set_threshold(row[5])
        
        return item

    @staticmethod
    def get_codes():
        codes = []

        query = """
        SELECT [Code] FROM [StoreManagement].[itm].[Item]
        """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        for row in rows:
            codes.append(row[0])

        return codes

    @staticmethod
    def add_item(code, name, quantity, price, threshold, risk, purchase):
        query = """
        INSERT INTO [StoreManagement].[itm].[Item]
        ([Code], [Name], [Quantity], [Price], [MinThreshold], [Risk], [AutoPurchaseOrder])
        VALUES
        ('%s', '%s', %s, %s, %s, %s, %s)
        """ % (code, name, quantity, price, threshold, risk, purchase)

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    @staticmethod
    def delete_item(code):
        query = """
        DELETE FROM [StoreManagement].[itm].[Item] WHERE [Code] = '%s'
        """ % code

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    @staticmethod
    def get_unit_types(code):
        units = []

        query = """
        SELECT [UnitName] FROM 
        [StoreManagement].[itm].[ItemAssociatedUnitType] WHERE
        [ItemCode] = '%s'
        """ % code

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        for row in rows:
            units.append(row[0])

        return units

    @staticmethod
    def update_item(code):
        return 0

    def __init__(self):
        self.code = None
        self.item = {}
        return
    
    def set_code(self, code):
        self.code = code
        return self
    
    def get_code(self):
        return self.code

    def set_name(self, name):
        self.item['name'] = name
        return self

    def get_name(self):
        return self.item['name']

    def set_risk(self, risk):
        self.item['risk'] = risk
        return self
    
    def get_risk(self):
        return self.item['risk']

    def set_price(self, price):
        self.item['price'] = price
        return self
    
    def get_price(self):
        return self.item['price']

    def set_quantity(self, quantity):
        self.item['quantity'] = quantity
        return self

    def get_quantity(self):
        return self.item['quantity']
    
    def set_threshold(self, threshold):
        self.item['threshold'] = threshold
        return self
    
    def get_threshold(self):
        return self.item['threshold']