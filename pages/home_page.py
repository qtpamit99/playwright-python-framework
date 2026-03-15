import time

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.price_utils import extract_price
from utils.waits import Wait
from utils.actions import Actions

logger = get_logger()


class HomePage(BasePage):

    def select_category(self, category_name):

        logger.info(f"Selecting category: {category_name}")

        # self.page.locator("#itemc", has_text=category_name).click() #
        Actions.safe_click(
            self.page.locator("#itemc", has_text=category_name)
        )

        # ✅ Smart wait
        Wait.for_visible(self.page, ".card")

        product_titles = self.page.locator(".card-title a").all_inner_texts()

        logger.info(f"Products loaded: {product_titles}")

        return len(product_titles) > 0

    def get_first_product_name(self):

        Wait.for_visible(self.page, ".card-title a")

        product_name = self.page.locator(".card-title a").first.inner_text()

        logger.info(f"📦 Product: {product_name}")

        return product_name

    def get_first_product_price(self):

        Wait.for_visible(self.page, ".card-block h5")

        product_price = self.page.locator(".card-block h5").first.inner_text()

        logger.info(f"💰 Price: {product_price}")

    def get_product_price(self):
        """Get price from product details page"""
        return extract_price(
            self.page.locator(".price-container").inner_text()
        )

    def select_product(self, product_name):
        """Select specific product dynamically"""

        product_locator = self.page.locator(
            ".card-title a",
            has_text=product_name
        )

        Wait.for_visible(self.page, ".card-title a")

       # product_locator.first.click()
        Actions.safe_click(product_locator)

    def wait_for_product_details(self):
        """Wait until product details page is fully loaded"""
        Wait.for_visible(self.page, ".name")

    def get_product_details(self):
        """Return product title & price from product details page"""

        Wait.for_visible(self.page, ".name")

        title = self.page.locator(".name").inner_text()

        price_text = self.page.locator(".price-container").inner_text()
        price = extract_price(price_text)

        return title, price

    def get_first_laptop_product(self):
        """Find first valid laptop product from UI"""

        laptop_keywords = ["sony", "vaio", "macbook", "dell"]

        Wait.for_visible(self.page, ".card-title a")

        product_titles = self.page.locator(".card-title a").all_inner_texts()

        for index, title in enumerate(product_titles):

            if any(keyword in title.lower() for keyword in laptop_keywords):

                print(f"   ✅ Laptop Selected → {title}")

                product_price = self.page.locator(".card-block h5").nth(index).inner_text()

                return title, product_price

        raise AssertionError("❌ No laptop products found in UI")

    def is_user_logged_in(self) -> bool:
        """Return True if logout button is visible."""
        return self.page.locator("#logout2").is_visible()

    def get_logged_in_username(self) -> str:
        """Return the username displayed in the navbar (e.g., 'Welcome amit054')."""
        return self.page.locator("#nameofuser").inner_text()

    def get_product_titles(self):
        """Return list of visible product titles"""
        Wait.for_visible(self.page, ".card-title a")
        #time.sleep(2)
        self.page.wait_for_function("""
            () => document.querySelectorAll('.card-title a').length > 0
        """)
        return self.page.locator(".card-title a").all_inner_texts()

    def get_product_price_by_index(self, index):
        """Return product price using product index"""
        return extract_price(
            self.page.locator(".card-block h5").nth(index).inner_text()
        )

    def go_home(self):
        """Force reload Home page (Demoblaze SPA Fix)"""

        logger.info("Reloading Home Page")

        self.page.locator("text=Home").click()

        #self.page.locator(".card").first.wait_for()
        Wait.for_visible(self.page, ".card")

    def get_product_price(self):
        return extract_price(
            self.page.locator(".price-container").inner_text()
        )

