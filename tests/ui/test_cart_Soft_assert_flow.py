import pytest

from utils.data_loader import load_test_data
from utils.price_utils import extract_price
from utils.soft_assert import SoftAssert
from utils.constants import CATEGORY_API_MAPPING
from utils.logger import get_logger

logger = get_logger()

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.flaky(reruns=2)
def test_laptop_data_driven_contract(pages, product_api, db_client):

    soft = SoftAssert()

    home = pages["home"]
    api = product_api

    logger.info(" DATA DRIVEN CONTRACT TEST STARTED")

    # Load Test Data
    test_data = load_test_data("test_data/products.yaml")["products"]

    # Dynamically filter laptop products
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
    # UI LAYER
    # ============================================================

    soft.equals(
        home.select_category(category),
        True,
        "Category selection failed"
    )

    ui_products = home.get_product_titles()

    logger.info(f" UI Products → {ui_products}")

    soft.not_empty(ui_products, "UI products list empty")

    for product in expected_products:
        soft.contains(
            product,
            ui_products,
            f"{product} missing in UI product list"
        )

    # ============================================================
    # API LAYER
    # ============================================================

    api_category = CATEGORY_API_MAPPING[category]

    api_products = api.get_products_by_category(api_category).get("Items", [])

    api_titles = [p["title"].strip() for p in api_products]

    logger.info(f" API Products → {api_titles}")

    soft.not_empty(api_titles, "API product list empty")

    for product in expected_products:
        soft.contains(
            product,
            api_titles,
            f"{product} missing in API response"
        )

    # ============================================================
    # PRODUCT MATCHING
    # ============================================================

    selected_product = expected_products[0]

    logger.info(f" Matching Product → {selected_product}")

    api_product = next(
        (p for p in api_products if p["title"].strip() == selected_product.strip()),
        None
    )

    soft.not_empty(api_product, "Product not found in API response")

    # ============================================================
    # DB VALIDATION
    # ============================================================

    db_product = db_client.get_product_by_name(selected_product)

    soft.not_empty(db_product, "Product not found in DB")

    if db_product:
        logger.info(f" DB Product → {db_product['title']}")

    # ============================================================
    # PRICE CONTRACT VALIDATION
    # ============================================================

    product_index = ui_products.index(selected_product)

    ui_price = home.get_product_price_by_index(product_index)
    api_price = int(api_product["price"]) if api_product else None
    db_price = int(db_product["price"]) if db_product else None

    logger.info(f" UI Price  → {ui_price}")
    logger.info(f" API Price → {api_price}")
    logger.info(f" DB Price  → {db_price}")

    soft.equals(ui_price, api_price, "UI vs API price mismatch")
    soft.equals(api_price, db_price, "API vs DB price mismatch")

    logger.info("CONTRACT VALIDATION COMPLETED")

    # ============================================================
    # FINAL SOFT ASSERT CHECK
    # ============================================================

    soft.assert_all()