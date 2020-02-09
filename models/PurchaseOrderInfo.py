from utils.Database import Database


class PurchaseOrderInfo:
    """Purchase Order Info Model"""

    @staticmethod
    def get_purchase_order_info(order_id):
        query = f"""
            SELECT
                [ItemCode],
                [Quantity],
                [isComplete],
                [completionDate]
            FROM
                [itm].[viewPurchaseOrderInfo]('{order_id}')
        """

        conn = Database.connect()
        cursor = conn.cursor()
        rows = Database.execute_query(query, cursor)
        conn.close()

        items = []

        for row in rows:
            item = PurchaseOrderInfo()
            item.set_item_code(row[0])
            item.set_quantity(row[1])
            item.set_is_complete(row[2])
            if row[3] is None:
                item.set_completion_date('Pending')
            else:
                item.set_completion_date(row[3])
            items.append(item)

        return items

    @staticmethod
    def confirm_delivery(order_id, item_code):
        query = f"""
            UPDATE
                [itm].[PurchaseOrderInfo]
            SET
                [isComplete] = 1
            WHERE
                [PurchaseOrderID] = '{order_id}'
                AND
                [ItemCode] = '{item_code}'
        """

        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    def __init__(self):
        self.item_code = None
        self.purchase_order_info = {}
        return

    def set_item_code(self, item_code):
        self.item_code = item_code
        return self

    def get_item_code(self):
        return self.item_code

    def set_quantity(self, quantity):
        self.purchase_order_info['quantity'] = quantity
        return self

    def get_quantity(self):
        return self.purchase_order_info['quantity']

    def set_is_complete(self, is_complete):
        self.purchase_order_info['is_complete'] = is_complete
        return self

    def get_is_complete(self):
        return self.purchase_order_info['is_complete']

    def set_completion_date(self, completion_date):
        self.purchase_order_info['completion_date'] = completion_date
        return self

    def get_completion_date(self):
        return self.purchase_order_info['completion_date']