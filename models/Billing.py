from utils.Database import Database


class Billing:

    @staticmethod
    def get_billing_rows():
        query = """
            SELECT DISTINCT
                [BillingMonth],
                [BillingYear]
            FROM 
                [StoreManagement].[itm].[DepartmentCosts]
            ORDER BY
            [BillingYear] DESC, [BillingMonth] DESC
            """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        billing_rows = []

        for row in rows:
            billing_row = Billing()
            billing_row.set_billing_month(row[0])
            billing_row.set_billing_year(row[1])
            billing_rows.append(billing_row)

        return billing_rows

    @staticmethod
    def get_department_billing(year, month):
        query = """
            SELECT 
                [DepartmentCode],
                [Total Price]
            FROM 
                [StoreManagement].[itm].[DepartmentCosts]
            WHERE
                [BillingYear] = 2020
                AND
                [BillingMonth] = 2
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        department_billing = []

        for row in rows:
            department = Billing()
            department.set_department_code(row[0])
            department.set_total(row[1])
            department_billing.append(department)

        return department_billing

    def __init__(self):
        self.department_code = None
        self.billing_info = {}
        return

    def set_department_code(self, department_code):
        self.department_code = department_code
        return self

    def get_department_code(self):
        return self.department_code

    def set_billing_month(self, billing_month):
        self.billing_info['billing_month'] = billing_month
        return self

    def get_billing_month(self):
        return self.billing_info['billing_month']

    def set_billing_year(self, billing_year):
        self.billing_info['billing_year'] = billing_year
        return self

    def get_billing_year(self):
        return self.billing_info['billing_year']

    def set_total(self, total):
        self.billing_info['total'] = total
        return self

    def get_total(self):
        return self.billing_info['total']
