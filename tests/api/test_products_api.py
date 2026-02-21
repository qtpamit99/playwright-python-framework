import pytest
import allure

from utils.schema_validator import SchemaValidator
from schemas.product_schema import PRODUCT_SCHEMA
from utils.logger import get_logger

logger = get_logger()


@pytest.mark.api
@allure.feature("API Schema Validation")
@allure.story("Product API Contract")
@pytest.mark.api
def test_product_schema_validation(product_api):

    logger.info("PRODUCT API SCHEMA TEST STARTED")

    response = product_api.get_products_by_category("phone")

    products = response.get("Items", [])

    # List validation
    SchemaValidator.validate_list(
        products,
        entity_name="Product List"
    )

    logger.info(f" Products Received → {len(products)}")

    #  Schema validation
    for product in products:

        SchemaValidator.validate(
            product,
            PRODUCT_SCHEMA,
            entity_name="Product"
        )

    logger.info("PRODUCT API SCHEMA TEST PASSED")