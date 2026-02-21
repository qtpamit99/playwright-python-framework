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
