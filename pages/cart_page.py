from utils.price_utils import extract_price
from utils.waits import Wait


class CartPage:

    def __init__(self, page):
        self.page = page

    def open_cart(self):
        """Navigate to cart"""
        self.page.locator("#cartur").click()

    def get_cart_product_names(self):
        """Fetch product names from cart"""
        return self.page.locator(".success td:nth-child(2)").all_inner_texts()

    def get_cart_product_prices(self):
        """Fetch product prices from cart"""
        return self.page.locator(".success td:nth-child(3)").all_inner_texts()

    def wait_for_cart_items(self):
        """Wait until cart items are visible"""
        Wait.for_visible(self.page, ".success")

