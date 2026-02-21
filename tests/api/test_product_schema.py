import pytest
import allure

from utils.schema_validator import SchemaValidator
from schemas.product_schema import PRODUCT_SCHEMA
from utils.logger import get_logger
logger = get_logger()


@pytest.mark.api
@allure.feature("API Schema Validation")
@allure.story("Product API Contract")
def test_product_schema_validation(product_api):

    logger.info("API SCHEMA VALIDATION STARTED")

    response = product_api.get_products_by_category("phone")

    products = response.get("Items", [])

    SchemaValidator.validate_list(products, entity_name="Product List")

    logger.info(f"Products Received → {len(products)}")

    for product in products:

        SchemaValidator.validate(
            product,
            PRODUCT_SCHEMA,
            entity_name="Product"
        )

    logger.info(" API SCHEMA VALIDATION PASSED")