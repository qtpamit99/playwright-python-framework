import pytest
import allure

from utils.data_loader import load_test_data
from utils.assertions import Assert
from utils.constants import CATEGORY_API_MAPPING
from utils.schema_validator import SchemaValidator
from schemas.product_schema import PRODUCT_SCHEMA
from utils.logger import get_logger

logger = get_logger()

test_data = load_test_data("test_data/products.yaml")["products"]


@pytest.mark.contract
@allure.feature("Contract Testing")
@allure.story("UI ↔ API Mapping Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("data", test_data)
@pytest.mark.smoke
@pytest.mark.api
def test_ui_api_product_mapping(pages, product_api, data):

    home = pages["home"]

    category = data["category"]
    product_name = data["product_name"]
    api_category = CATEGORY_API_MAPPING[category]

    logger.info(f" CONTRACT TEST → {product_name}")

    # ================= UI =================
    with allure.step(f"UI → Load Product [{product_name}]"):

        home.select_category(category)
        home.select_product(product_name)

        ui_title, ui_price = home.get_product_details()

        logger.info(f"UI Title → {ui_title}")
        logger.info(f"UI Price → {ui_price}")

        Assert.contains(product_name, ui_title)

    # ================= API =================
    with allure.step("API → Fetch Product"):

        response = product_api.get_products_by_category(api_category)
        products = response.get("Items", [])

        Assert.not_empty(products)

        api_product = next(
            (p for p in products if p["title"].strip() == product_name),
            None
        )

        Assert.not_empty(api_product)

        #  CONTRACT VALIDATION
        SchemaValidator.validate(
            api_product,
            PRODUCT_SCHEMA,
            "API Product"
        )

        api_price = int(api_product["price"])

        logger.info(f"API Price → {api_price}")

    # ================= CONTRACT =================
    with allure.step(" UI ↔ API Contract Validation"):

        Assert.equals(ui_price, api_price)