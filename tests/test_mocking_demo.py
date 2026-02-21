import json
import os

from utils.waits import Wait
from utils.assertions import Assert
from utils.logger import get_logger
from utils.schema_validator import SchemaValidator
from schemas.product_schema import PRODUCT_SCHEMA

logger = get_logger()


def test_mocked_products(pages, page):

    logger.info("👑 MOCKING DEMO TEST STARTED")

    # Safe file path
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "test_data", "mock_products.json")

    with open(file_path) as f:
        mock_data = json.load(f)

    logger.info("📡 Mock API response loaded")

    # ============================================================
    #  API MOCKING
    # ============================================================

    page.route("**/bycat", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(mock_data)
    ))

    logger.info(" API interception active")

    home = pages["home"]

    # ============================================================
    #  UI INTERACTION (POM Driven )
    # ============================================================

    home.select_category("Laptops")

    Wait.for_visible(page, ".card-title a")

    product_name = page.locator(".card-title a").first.inner_text()
    product_price = page.locator(".card-block h5").first.inner_text()

    logger.info(f"UI Product → {product_name}")
    logger.info(f" UI Price   → {product_price}")

    # ============================================================
    #  MOCK CONTRACT VALIDATION
    # ============================================================

    SchemaValidator.validate_list(mock_data.get("Items"), "Mock API")

    first_product = mock_data["Items"][0]

    SchemaValidator.validate(
        first_product,
        PRODUCT_SCHEMA,
        "Mock Product"
    )

    logger.info(" Mock schema validation passed")

    # ============================================================
    # BUSINESS ASSERTION
    # ============================================================

    Assert.contains("Amit Super Laptop", product_name)

    logger.info(" MOCKING TEST PASSED")