from utils import Database

class Unit:
    """ Unit Model """

    @staticmethod
    def getAllUnits():
        query = "SELECT * FROM [StoreManagement].[itm].[Unit]"

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        unit = []

        for row in rows:
            print(row)

        return unit

    @staticmethod
    def getUnits(id):
        unit = Unit()
        return unit

    @staticmethod
    def getUnitsBy(key, value):
        unit = []
        return unit

    def __init__(self):
        self.UnitName = None
        self.unit = {}
        return

    def Insert(self):
        if self.UnitName == None:
            Database.execute(
                "INSERT INTO [StoreManagement].[itm].[Unit] ('unit_name', 'val', 'data_type') VALUES (%s, %s, %s)",
                (self.unit['unit_name'], self.unit['val'], self.unit['data_type']))

            rows = Database.get_rows('SELECT LAST_INSERT_ID() AS insert_id')
            self.UnitName = rows[0]['insert_id']

    def Delete(self):
        if self.UnitName == None:
            return
        else:
            Database.execute("DELETE FROM [StoreManagement].[itm].[Unit] WHERE UnitName = %s", (self.UnitName,))

    def setUnitName(self, unit_name):
        self.unit['unit_name'] = unit_name
        return self

    def getUnitName(self):
        return self.unit['unit_name']

    def setVal(self, val):
        self.unit['val'] = val
        return self

    def getVal(self):
        return self.unit['val']

    def setDataType(self, data_type):
        self.unit['data_type'] = data_type
        return self

    def getDataType(self):
        return self.unit['data_type']