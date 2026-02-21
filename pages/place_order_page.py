from pages.base_page import BasePage


class PlaceOrderPage(BasePage):

    def place_order(self, order_data):

        self.page.locator("//button[normalize-space()='Place Order']").click()
        self.page.locator("#name").fill(order_data["name"])
        self.page.locator("#country").fill(order_data["country"])
        self.page.locator("#city").fill(order_data["city"])
        self.page.locator("#card").fill(order_data["card"])
        self.page.locator("#month").fill(order_data["month"])
        self.page.locator("#year").fill(order_data["year"])

        self.page.locator("text=Purchase").click()

    def get_confirmation_details(self):
        return self.page.locator(".sweet-alert").inner_text()
