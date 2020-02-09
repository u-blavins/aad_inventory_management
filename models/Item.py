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
            [MinThreshold],
            [AutoPurchaseOrder]
            FROM [StoreManagement].[itm].[Item]
            WHERE [onDisplay] = 1
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
            item.set_purchase_order(row[6])
            items.append(item)

        return items

    @staticmethod
    def get_item(code):
        item = None

        query = """
        SELECT [Code], [Name], [Risk], [Price],
            [Quantity],
            [MinThreshold], [AutoPurchaseOrder] FROM
        [itm].[Item] WHERE [Code] = '%s'
        AND [onDisplay] = 1
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
            item.set_purchase_order(row[6])
    
        return item

    @staticmethod
    def get_codes():
        codes = []

        query = """
        SELECT [Code] FROM [StoreManagement].[itm].[Item]
        WHERE [onDisplay] = 1
        """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()
        for row in rows:
            codes.append(row[0])

        return codes

    @staticmethod
    def add_item(code, name, quantity, price, threshold, unit_types, risk, purchase):
        query = """
        INSERT INTO [StoreManagement].[itm].[Item]
        ([Code], [Name], [Quantity], [Price], [MinThreshold], [Risk], [AutoPurchaseOrder])
        VALUES
        ('%s', '%s', %s, %s, %s, %s, %s)
        """ % (code, name, quantity, price, threshold, risk, purchase)

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)

        for unit in unit_types:
            query = """
            INSERT INTO 
                [itm].[ItemAssociatedUnitType]([ItemCode],[UnitName])
            VALUES
                ('%s','%s')
            """ % (code, unit)
            Database.execute_non_query(query,cursor)

        cursor.commit()
        conn.close()

    @staticmethod
    def delete_item(code):
        query = """
        UPDATE [StoreManagement].[itm].[Item] SET [onDisplay] = 0 WHERE [Code] = '%s'
        """ % code

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    
    @staticmethod
    def edit_item(code, name, quantity, price, threshold, risk, purchase):
        query = f"""
        UPDATE 
            [StoreManagement].[itm].[Item]
        SET 
            [Name] = '{name}', [Quantity] = {quantity}, [Price] = {price}, [MinThreshold] = {threshold}, [Risk] = {risk}, [AutoPurchaseOrder] = {purchase}
        WHERE 
            [Code] = '{code}'
        """

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    @staticmethod
    def is_risk_item(code):
        query = f"""
        SELECT [Risk] FROM [StoreManagement].[itm].[Item] WHERE [Code] = '{code}'
        """ 
        conn = Database.connect()
        cursor = conn.cursor()
        result = Database.execute_query(query, cursor)
        cursor.commit()
        conn.close()
        return result[0][0]

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

    def set_purchase_order(self, purchase):
        self.item['purchase'] = purchase
        return self

    def get_purchase_order(self):
        return self.item['purchase']
