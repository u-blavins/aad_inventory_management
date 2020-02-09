from utils.Database import Database


class PurchaseOrder:
    """Purchase Order Model"""

    @staticmethod
    def get_purchase_orders_pending():
        query = """
            SELECT
                [PurchaseOrderID],
                [Email],
                [GeneratedDate]
            FROM
                [itm].[PendingPurchaseOrders]
            ORDER BY
                [GeneratedDate] DESC
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        purchase_orders = []

        for row in rows:
            purchase_order = PurchaseOrder()
            purchase_order.set_purchase_order_id(row[0])
            purchase_order.set_generated_by(row[1])
            purchase_order.set_generated_date(row[2])
            purchase_orders.append(purchase_order)

        return purchase_orders

    @staticmethod
    def get_purchase_orders_history():
        query = """
            SELECT
                [PurchaseOrderID],
                [Email],
                [GeneratedDate],
                [CompletionDate]
            FROM
                [itm].[PurchaseOrdersHistory]
            ORDER BY
                [CompletionDate], [GeneratedDate] DESC
        """
        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        purchase_orders = []

        for row in rows:
            purchase_order = PurchaseOrder()
            purchase_order.set_purchase_order_id(row[0])
            purchase_order.set_generated_by(row[1])
            purchase_order.set_generated_date(row[2])
            purchase_order.set_completion_date(row[3])
            purchase_orders.append(purchase_order)

        return purchase_orders

    def __init__(self):
        self.purchase_order_id = None
        self.purchase_order = {}
        return

    def set_purchase_order_id(self, purchase_order_id):
        self.purchase_order_id = purchase_order_id
        return self

    def get_purchase_order_id(self):
        return self.purchase_order_id

    def set_generated_by(self, generated_by):
        self.purchase_order['generated_by'] = generated_by
        return self

    def get_generated_by(self):
        return self.purchase_order['generated_by']

    def set_generated_date(self, generated_date):
        self.purchase_order['generated_date'] = generated_date
        return self

    def get_generated_date(self):
        return self.purchase_order['generated_date']

    def set_completion_date(self, completion_date):
        self.purchase_order['completion_date'] = completion_date
        return self

    def get_completion_date(self):
        return self.purchase_order['completion_date']

