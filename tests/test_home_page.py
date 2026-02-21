import pytest

from tests.contract.test_ui_api_mapping import test_data
from utils.assertions import Assert
from utils.constants import CATEGORY_API_MAPPING
from utils.logger import get_logger

logger = get_logger()


@pytest.mark.parametrize("data", test_data)
def test_product_contract_validation(pages, product_api, db_client, data):

    home = pages["home"]
    api = product_api

    category = data["category"]
    product_name = data["product_name"]

    logger.info(f" CONTRACT TEST → {product_name}")

    # UI
    home.select_category(category)
    home.select_product(product_name)

    ui_price = home.get_product_price()

    # API
    api_category = CATEGORY_API_MAPPING[category]
    api_products = api.get_products_by_category(api_category).get("Items", [])

    api_product = next(
        (p for p in api_products if p["title"].strip() == product_name.strip()),
        None
    )

    Assert.not_empty(api_product, f"Product missing in API → {product_name}")

    api_price = int(float(api_product["price"]))

    # DB
    db_product = db_client.get_product_by_name(product_name)

    Assert.not_empty(db_product, f"Product missing in DB → {product_name}")

    db_price = int(float(db_product["price"]))

    # CONTRACT ASSERTION
    Assert.equals(ui_price, api_price, "UI vs API mismatch")
    Assert.equals(api_price, db_price, "API vs DB mismatch")