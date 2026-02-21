import pytest

from utils.data_loader import load_test_data
from utils.price_utils import extract_price
from utils.assertions import Assert
from utils.constants import CATEGORY_API_MAPPING
from utils.logger import get_logger

logger = get_logger()


@pytest.mark.flaky(reruns=0)
def test_laptop_data_driven_contract(pages, product_api, db_client):

    home = pages["home"]
    api = product_api

    logger.info(" DATA DRIVEN CONTRACT TEST STARTED")

    #  Load Test Data (NO YAML CHANGE)
    test_data = load_test_data("test_data/products.yaml")["products"]

    #  Dynamically filter laptop products
    laptop_products = [
        item["product_name"]
        for item in test_data
        if item["category"] == "Laptops"
    ]

    category = "Laptops"
    expected_products = laptop_products

    logger.info(f"Category → {category}")
    logger.info(f"Expected Products → {expected_products}")

    # ============================================================
    #  UI LAYER
    # ============================================================

    Assert.equals(home.select_category(category), True)

    ui_products = home.get_product_titles()

    logger.info(f" UI Products → {ui_products}")

    Assert.not_empty(ui_products)

    for product in expected_products:
        Assert.contains(product, ui_products)

    # ============================================================
    #  API LAYER
    # ============================================================

    api_category = CATEGORY_API_MAPPING[category]

    api_products = api.get_products_by_category(api_category).get("Items", [])

    api_titles = [p["title"].strip() for p in api_products]

    logger.info(f" API Products → {api_titles}")

    Assert.not_empty(api_titles)

    for product in expected_products:
        Assert.contains(product, api_titles)

    # ============================================================
    #  PRODUCT MATCHING
    # ============================================================

    selected_product = expected_products[0]

    logger.info(f" Matching Product → {selected_product}")

    api_product = next(
        (p for p in api_products if p["title"].strip() == selected_product.strip()),
        None
    )

    Assert.not_empty(api_product)

    # ============================================================
    #  DB VALIDATION (NAME BASED )
    # ============================================================

    db_product = db_client.get_product_by_name(selected_product)

    Assert.not_empty(db_product)

    logger.info(f" DB Product → {db_product['title']}")

    # ============================================================
    #  PRICE CONTRACT VALIDATION
    # ============================================================

    product_index = ui_products.index(selected_product)

    ui_price = home.get_product_price_by_index(product_index)
    api_price = int(api_product["price"])
    db_price = int(db_product["price"])

    logger.info(f" UI Price  → {ui_price}")
    logger.info(f" API Price → {api_price}")
    logger.info(f" DB Price  → {db_price}")

    Assert.equals(ui_price, api_price)
    Assert.equals(api_price, db_price)

    logger.info("CONTRACT VALIDATION PASSED")