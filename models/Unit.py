from utils.Database import Database

class Unit:
    """ Unit Model """

    @staticmethod
    def get_all_units():
        units = []

        query = """
        SELECT * FROM [StoreManagement].[itm].[Unit]
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        for row in rows:
            unit = Unit()
            unit.set_name(row[0])
            unit.set_value(row[1])
            units.append(unit)

        return units
    
    @staticmethod
    def get_unit(name):
        unit = None

        query = """
        SELECT * FROM [StoreManagement].[itm].[Unit] WHERE
        [UnitName] = '%s'
        """ % name

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        if len(rows) != 0:
            for row in rows:
                unit = Unit()
                unit.set_name(row[0])
                unit.set_value(row[1])

        return unit

    def __init__(self):
        self.name = None
        self.value = None
        return
    
    def set_name(self, name):
        self.name = name
        return self

    def get_name(self):
        return self.name

    def set_value(self, value):
        self.value = value
        return self

    def get_value(self):
        return self.value
