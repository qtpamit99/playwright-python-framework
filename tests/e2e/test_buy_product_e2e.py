import pytest
import allure

from utils.actions import Actions
from utils.data_loader import load_test_data
from utils.assertions import Assert
from utils.price_utils import extract_price
from utils.config_manager import get_credentials, load_environment_config
from utils.session_manager import SessionManager
from utils.token_manager import TokenManager
from utils.test_data_generator import generate_order_data
from utils.constants import CATEGORY_API_MAPPING

from api_clients.product_api import ProductAPI


# ============================================================
# 📊 TEST DATA
# ============================================================
test_data = load_test_data("test_data/products.yaml")["products"]


# ============================================================
# 👑 TEST CASE
# ============================================================
@allure.title("End-to-End Purchase Flow with UI + API + DB Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.regression
def test_full_purchase_flow(pages, page, api_request, db_client, request):

    home = pages["home"]
    cart = pages["cart"]
    order = pages["order"]

    env_name = request.config.getoption("--env")
    env_config = load_environment_config(env_name)

    api = ProductAPI(api_request, env_config)

    # LOGIN
    with allure.step("🔐 Login via UI"):

        username, password = get_credentials(env_name)

        login_page = SessionManager.login(page, username, password)

        Assert.equals(login_page.is_logout_visible(), True)

        token, token_source = TokenManager.find_token(page)
        Assert.not_empty(token)

    # CLEAN CART
    with allure.step("Clean Cart Before Test"):

        cart.open_cart()
        home.go_home()

    expected_total = 0

    # PRODUCT LOOP
    for data in test_data:

        category = data["category"]
        product_name = data["product_name"]

        with allure.step(f" Category → {category}"):

            home.select_category(category)

        with allure.step(f" Product → {product_name}"):

            home.select_product(product_name)
            home.wait_for_product_details()

            ui_price = extract_price(
                page.locator(".price-container").inner_text()
            )

        with allure.step(" API Validation"):

            api_category = CATEGORY_API_MAPPING[category]

            api_products = api.get_products_by_category(api_category).get("Items", [])

            api_product = next(
                (p for p in api_products if p["title"].strip() == product_name.strip()),
                None
            )

            Assert.not_empty(api_product)

            api_price = int(float(api_product["price"]))

            Assert.equals(ui_price, api_price)

        with allure.step(" DB Validation"):

            db_product = db_client.get_product_by_name(product_name)

            Assert.not_empty(db_product)

            db_price = int(float(db_product["price"]))

            Assert.equals(api_price, db_price)

        with allure.step(" Add To Cart"):

            with Actions.accept_dialog(page):
                page.locator("text=Add to cart").click()

        expected_total += ui_price

        home.go_home()

    #  CART VALIDATION
    with allure.step("Cart Validation"):

        cart.open_cart()
        cart.wait_for_cart_items()

        cart_total = sum(
            extract_price(p) for p in cart.get_cart_product_prices()
        )

        Assert.equals(expected_total, cart_total)

    # PLACE ORDER
    with allure.step(" Place Order"):

        order.place_order(generate_order_data())

    # CONFIRMATION
    with allure.step(" Purchase Validation"):

        confirmation_text = order.get_confirmation_details()

        Assert.contains("Thank you for your purchase!", confirmation_text)
        Assert.contains(str(expected_total), confirmation_text)