from utils import Database

class Unit:
    """ Unit Model """

    @staticmethod
    def get_all_units():
        units = []

        query = """
        SELECT * FROM [StoreManagement].[itm].[Unit]
        """
        rows = Database.execute_query(query)

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

        rows = Database.execute_query(query)

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