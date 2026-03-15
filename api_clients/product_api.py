class ProductAPI:

    def __init__(self, request_context, env_config):
        self.request = request_context
        self.api_url = env_config["api_url"]

    def get_products_by_category(self, category):

        response = self.request.post(
            "/bycat",
            data={"cat": category}
        )

        assert response.status == 200, f"API failed: {response.status}"

        return response.json()

    def get_product_price(self, category, product_name):
        products = self.get_products_by_category(category).get("Items", [])

        product = next(
            (p for p in products if p["title"].strip() == product_name.strip()),
            None
        )

        return int(float(product["price"]))
