import mysql.connector


class DBClient:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Synup@123",
            database="demoblaze_test"
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def get_product_by_name(self, product_name):
        query = """
            SELECT * 
            FROM products
            WHERE title = %s
        """

        self.cursor.execute(query, (product_name,))
        return self.cursor.fetchone()

    def get_product_by_id(self, product_id):
        """Fetch product using product ID"""

        query = """
            SELECT *
            FROM products
            WHERE id = %s
        """

        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_product_price(self, product_name):
        product = self.get_product_by_name(product_name)

        if not product:
            raise AssertionError(f"Product not found in DB: {product_name}")

        return int(float(product["price"]))
